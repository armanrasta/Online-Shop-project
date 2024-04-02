from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Customer
from core.RedisConf import redis_client
import uuid
import re
from django.contrib.auth import authenticate

#sign up
@api_view(['POST'])
def signup_otp(request):
    if request.method == 'POST':
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
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
        user_info = f'{email},{username},{first_name},{last_name},{password}'
        redis_client.setex(user_info_key, 300, user_info)

        otp_code = get_random_string(length=6, allowed_chars='0123456789')
        otp_key = f'otp:{user_id}'
        redis_client.setex(otp_key, 300, otp_code)
        
        subject = 'Sign Up OTP'
        message = f'Your OTP for sign up is: \n {otp_code}'
        send_mail(subject, message, 'sender@example.com', [email])

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
        user_info = redis_client.get(user_info_key)
        if not user_info:
            return Response({'error': 'User information not found'},
                            status=status.HTTP_404_NOT_FOUND)

        email, username, first_name, last_name, password = user_info.split(',')
        #create user
        Customer.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
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
        email_or_username = request.data.get('username or email')
        password = request.data.get('password')
        
        #checking if the client entered username or email
        pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
        
        if pattern.match(email_or_username):
            email = email_or_username
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            username = email_or_username
            try:
                user = Customer.objects.get(username=username)
                email = user.email
            except Customer.DoesNotExist:
                return Response({'error': 'User with this username does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        #check password
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        message = f'Your OTP for Log-IN is: \n {otp_code}'
        send_mail(subject, message, 'sender@example.com', [email])
        
        return Response({'success': 'OTP sent to your email', 'user_id': user_id}, status=status.HTTP_200_OK)
        
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        otp_code = request.data.get('otp')
        user_id = request.data.get('user_id')
        
        #verify OTP
        otp_key = f'otp:{user_id}'
        stored_otp = redis_client.get(otp_key)
        if not stored_otp or stored_otp.decode('utf-8') != otp_code:
            return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
        
        #get user information
        user_info_key = f'user_info:{user_id}'
        user_info = redis_client.get(user_info_key)
        if not user_info:
            return Response({'error': 'User information not found'}, status=status.HTTP_404_NOT_FOUND)
        
        #parse user information
        email, password = user_info.decode('utf-8').split(',')
        
        #authenticate user
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        #generate JWT token
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        #delete OTP and user information from Redis
        redis_client.delete(otp_key)
        redis_client.delete(user_info_key)
        
        return Response(data, status=status.HTTP_200_OK)
        
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
     
@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email_or_username = request.data.get('username or email')
        if not email_or_username:
            return Response({'error': 'Email or Username is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        otp = request.data.get('otp')
        if not otp:
            return Response({'error': 'One Time Password is required'},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)