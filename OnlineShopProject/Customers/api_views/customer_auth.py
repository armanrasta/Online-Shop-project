from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ..models import Customer, Cart, CartItem
from Product.models import Product
from core.RedisConf import redis_client
from django.contrib.auth import authenticate
import uuid
import re
import json



#sign up
@api_view(['POST'])
def signup_otp(request):
    if request.method == 'POST':
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        password = request.data.get('password')
        
        #email validation check
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        #checking if username or email is taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = uuid.uuid4().hex

        user_info_key = f'user_info:{user_id}'
        user_info = f'{email},{username},{phone_number},{first_name},{last_name},{password}'
        redis_client.setex(user_info_key, 300, user_info)

        otp_code = get_random_string(length=6, allowed_chars='0123456789')
        otp_key = f'otp:{user_id}'
        redis_client.setex(otp_key, 300, otp_code)
        
        subject = 'Sign Up OTP'
        message = f'Your OTP for sign up is: \n {otp_code}'
        send_mail(subject, message, 'armanrostami1000@gmail.com', [email])

        return Response({'success': 'OTP sent to your email', 'user_id': user_id},
                        status=status.HTTP_200_OK)

    return Response({'error': 'Method not allowed'}, 
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_account(request):
    
    if request.method == 'POST':
        otp_code = request.data.get('otp')
        user_id = request.data.get('user_id')
        
        #otp check
        otp_key = f'otp:{user_id}'
        stored_otp = redis_client.get(otp_key)
        if not stored_otp or stored_otp.decode('utf-8') != otp_code:
            return Response({'error': 'Invalid OTP code'},
                            status=status.HTTP_400_BAD_REQUEST)
            
        #redis user info parsing
        user_info_key = f'user_info:{user_id}'
        user_info_bytes = redis_client.get(user_info_key)
        if not user_info_bytes:
            return Response({'error': 'User information not found'},
                            status=status.HTTP_404_NOT_FOUND)
        user_info = user_info_bytes.decode('utf-8')
        email, username, phone_number, first_name, last_name, password = user_info.split(',')
        #create user
        Customer.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number = phone_number,
            email=email,
            password=password
        )
        
        redis_client.delete(otp_key)
        redis_client.delete(user_info_key)

        return Response({'success': 'Account created successfully'},
                        status=status.HTTP_201_CREATED)

    return Response({'error': 'Method not allowed'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

#login
@api_view(['POST'])
def login_otp(request):
    
    if request.method == 'POST':
        email_or_username = request.data.get('username-or-email')
        password = request.data.get('password')
        
        #checking if the client entered username or email
        pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
        
        if pattern.match(email_or_username):
            email = email_or_username
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
        else:
            username = email_or_username
            try:
                user = Customer.objects.get(username=username)
                email = user.email
            except Customer.DoesNotExist:
                return Response({'error': 'User with this username does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)
        
        #check password
        if not user.check_password(password):
            return Response({'error': 'Invalid password'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        #create user ID
        user_id = uuid.uuid4().hex
        
        #storing user info
        user_info = f'{email},{password}'
        user_info_key = f'user_info:{user_id}'
        redis_client.setex(user_info_key, 300, user_info)
        
        #generate OTP and store it
        otp_code = get_random_string(length=6, allowed_chars='0123456789')
        otp_key = f'otp:{user_id}'
        redis_client.setex(otp_key, 300, otp_code)
        
        #sending email
        subject = 'Log-IN OTP'
        message = f'Your OTP for Log-IN is: \n {otp_code}\n***Expires in 5 minutes***'
        send_mail(subject, message, 'armanrostami1000@gmail.com', [email])
        
        
        return Response({'success': 'OTP sent to your email', 'user_id': user_id},
                        status=status.HTTP_200_OK)
        
    return Response({'error': 'Method not allowed'}, 
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        otp_code = request.data.get('otp')
        user_id = request.data.get('user_id')
        
        #verify OTP
        otp_key = f'otp:{user_id}'
        stored_otp = redis_client.get(otp_key)
        if not stored_otp or stored_otp.decode('utf-8') != otp_code:
            return Response({'error': 'Invalid OTP code'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        #get user information
        user_info_key = f'user_info:{user_id}'
        user_info = redis_client.get(user_info_key)
        if not user_info:
            return Response({'error': 'User information not found'},
                            status=status.HTTP_404_NOT_FOUND)
        
        #parse user information
        email, password = user_info.decode('utf-8').split(',')
        print("Email:", email.strip())
        print("Password:", password.strip())
        
        #authenticate user
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is None:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        #generate JWT token
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        #transfer cart items from cookie to database
        cart_items_cookie = request.COOKIES.get('cookie_cart', '[]')
        cart_items_cookie = json.loads(cart_items_cookie)
        
        cart, created = Cart.objects.get_or_create(customer=user)
        for item in cart_items_cookie:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        
        #delete OTP and user information from Redis and cookie
        redis_client.delete(otp_key)
        redis_client.delete(user_info_key)
        response = Response(data, status=status.HTTP_200_OK)
        response.delete_cookie('cart_items')
        
        return response
    else:
        return Response({'error': 'Method not allowed'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#password request
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
def request_password_reset(request):
    email_or_username = request.data.get('username_or_email')
    if not email_or_username:
        return Response({'error': 'Email or Username is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Find user by email or username
    try:
        user = User.objects.get(email=email_or_username) if '@' in email_or_username else User.objects.get(username=email_or_username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    password_reset_url = f'http://example.com/password_reset/{uid}/{token}/'

    subject = 'Password Reset Request'
    message = f'Please use the link below to reset your password:\n{password_reset_url}'
    send_mail(subject, message, 'armanrostami1000@gmail.com', [user.email])

    return Response({'success': 'Password reset link sent to your email'}, 
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request, uidb64, token):
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not new_password or not confirm_password:
        return Response({'error': 'New password and confirmation are required'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token or UID'}, status=status.HTTP_400_BAD_REQUEST)
