from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Customer
from core.RedisConf import redis_client
import uuid

@api_view(['POST'])
def send_otp(request):
    if request.method == 'POST':
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Generate unique identifier for the user
        user_id = uuid.uuid4().hex
        
        # Store user information and OTP in Redis
        user_info_key = f'user_info:{user_id}'
        user_info = f'{email},{username},{first_name},{last_name},{password}'
        redis_client.setex(user_info_key, 300, user_info)
        
        # Generate OTP
        otp_code = get_random_string(length=6, allowed_chars='0123456789')
        otp_key = f'otp:{user_id}'
        redis_client.setex(otp_key, 300, otp_code)
        
        # Send email
        subject = 'Sign Up OTP'
        message = f'Your OTP for sign up is: {otp_code}'
        send_mail(subject, message, 'sender@example.com', [email])

        return Response({'success': 'OTP sent to your email', 'user_id': user_id}, status=status.HTTP_200_OK)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_account(request):
    if request.method == 'POST':
        otp_code = request.data.get('otp')
        user_id = request.data.get('user_id')  # User ID passed from the previous view
        
        # Verify OTP
        otp_key = f'otp:{user_id}'
        stored_otp = redis_client.get(otp_key)
        if not stored_otp or stored_otp.decode('utf-8') != otp_code:
            return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

        # Get user information
        user_info_key = f'user_info:{user_id}'
        user_info = redis_client.get(user_info_key)
        if not user_info:
            return Response({'error': 'User information not found'}, status=status.HTTP_404_NOT_FOUND)

        # Parse user information
        email, username, first_name, last_name, password = user_info.split(',')

        # Create user account
        user = Customer.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        
        # Delete OTP and user information from Redis
        redis_client.delete(otp_key)
        redis_client.delete(user_info_key)

        return Response({'success': 'Account created successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email_or_username = request.data.get('username or email')
        if not email_or_username:
            return Response({'error': 'Email or Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = request.data.get('otp')
        if not otp:
            return Response({'error': 'One Time Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email_or_username = request.data.get('username or email')
        password = request.data.get('password')
        otp = request.data.get('otp')

        form = OTPAuthenticationForm(request, data={'username': email_or_username, 'password': password})
        if form.is_valid():
            user = form.get_user()
            if user:
                # Check if the user has an email OTP device
                email_device = None
                for device in devices_for_user(user):
                    if isinstance(device, EmailDevice):
                        email_device = device
                        break

                if email_device:
                    # Generate OTP code
                    otp_code = email_device.generate_challenge()

                    # Send OTP code to user's email
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is: {otp_code}',
                        'armanrostamiar@gmail.com',  # Replace with your email address
                        [email_device.confirmed_email],
                        fail_silently=False,
                    )

                    # Generate JWT token for the user
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    # Return success response with JWT token
                    return Response({'access_token': access_token}, status=status.HTTP_200_OK)
                else:
                    # No email OTP device found for the user
                    return Response({'error': 'Email OTP device not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # User not found
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Username/email or password is incorrect
            return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Only POST method is allowed
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
