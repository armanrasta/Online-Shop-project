from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django_otp import devices_for_user
from django_otp.plugins.otp_static.models import StaticDevice
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

#otp API
@api_view(['POST'])
def send_otp_email(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        device = devices_for_user(user, StaticDevice)
        if not device:
            device = StaticDevice.objects.create(user=user, name='OTP Device')

        otp_token = get_random_string(length=6, allowed_chars='0123456789')
        device.token_set.create(token=otp_token)

        subject = 'Login OTP'
        message = f'Your OTP for login is: {otp_token}'
        send_mail(subject, message, 'sender@example.com', [email])

        return Response({'success': 'OTP sent successfully'}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def sign_up_with_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_409_CONFLICT)

        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        otp_token = get_random_string(length=6, allowed_chars='0123456789')

        
        user.profile.otp_token = otp_token
        user.profile.save()

        subject = 'Sign Up OTP'
        message = f'Your OTP for sign up is: {otp_token}'
        send_mail(subject, message, 'sender@example.com', [email])

        return Response({'success': 'Sign up successful. OTP sent to your email'}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
