from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django_otp import devices_for_user
from django_otp.plugins.otp_static.models import StaticDevice
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer

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

        if Customer.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_409_CONFLICT)

        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        first_name = request.data.get('first name')
        if not first_name:
            return Response({'error': 'First name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        last_name = request.data.get('last name')
        if not last_name:
            return Response({'error': 'Last name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = Customer.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        otp_token = get_random_string(length=6, allowed_chars='0123456789')

        
        user.profile.otp_token = otp_token
        user.profile.save()

        subject = 'Sign Up OTP'
        message = f'Your OTP for sign up is: {otp_token}'
        send_mail(subject, message, 'sender@example.com', [email])

        return Response({'success': 'Sign up successful. OTP sent to your email'}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST']) #imcomplete
def login(request):
    if request.method == 'POST':
        email_or_username= request.data.get('username or email') 
        if not email_or_username:
            return Response({'error': 'Email or Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = request.data.get('otp')
        if not otp:
            return Response({'error': 'One Time Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email_or_username= request.data.get('username or email') 
        if not email_or_username:
            return Response({'error': 'Email or Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = request.data.get('otp')
        if not otp:
            return Response({'error': 'One Time Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
# from django.core.mail import send_mail
# from django_otp import devices_for_user
# from django_otp.plugins.otp_email.models import EmailDevice
# from django_otp.forms import OTPAuthenticationForm
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         email_or_username = request.data.get('username or email')
#         password = request.data.get('password')
#         otp = request.data.get('otp')

#         # Authenticate the user with their username/email and password
#         form = OTPAuthenticationForm(request, data={'username': email_or_username, 'password': password})
#         if form.is_valid():
#             user = form.get_user()
#             if user:
#                 # Check if the user has an email OTP device
#                 email_device = None
#                 for device in devices_for_user(user):
#                     if isinstance(device, EmailDevice):
#                         email_device = device
#                         break

#                 if email_device:
#                     # Generate OTP code
#                     otp_code = email_device.generate_challenge()

#                     # Send OTP code to user's email
#                     send_mail(
#                         'Your OTP Code',
#                         f'Your OTP code is: {otp_code}',
#                         'your_email@example.com',  # Replace with your email address
#                         [email_device.confirmed_email],
#                         fail_silently=False,
#                     )

#                     # Generate JWT token for the user
#                     refresh = RefreshToken.for_user(user)
#                     access_token = str(refresh.access_token)

#                     # Return success response with JWT token
#                     return Response({'access_token': access_token}, status=status.HTTP_200_OK)
#                 else:
#                     # No email OTP device found for the user
#                     return Response({'error': 'Email OTP device not found'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 # User not found
#                 return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Username/email or password is incorrect
#             return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         # Only POST method is allowed
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
