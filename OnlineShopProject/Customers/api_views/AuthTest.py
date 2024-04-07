from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.RedisConf import redis_client

class SignUpOTPTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_otp(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('signup_otp'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

class CreateAccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_account(self):
        # Simulate OTP verification by creating a valid OTP code
        otp_code = '123456'
        user_id = 'some_user_id'
        redis_client.set(f'otp:{user_id}', otp_code)

        data = {
            'otp': otp_code,
            'user_id': user_id
        }
        response = self.client.post(reverse('create_account'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)

class LoginOTPTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_otp(self):
        data = {
            'username_or_email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login_otp'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login(self):
        # Simulate OTP verification by creating a valid OTP code
        otp_code = '123456'
        user_id = 'some_user_id'
        redis_client.set(f'otp:{user_id}', otp_code)
        user_info = 'test@example.com,testpassword'
        redis_client.set(f'user_info:{user_id}', user_info)

        data = {
            'otp': otp_code,
            'user_id': user_id
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

# class PasswordResetTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_request_password_reset(self):
#         data = {
#             'username_or_email': 'test@example.com'
#         }
#         response = self.client.post(reverse('request_password_reset'), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('success', response.data)

#     def test_reset_password(self):
#         # Assume valid token and UID for password reset
#         uidb64 = 'some_uid'
#         token = 'some_valid_token'
#         data = {
#             'new_password': 'newpassword',
#             'confirm_password': 'newpassword'
#         }
#         response = self.client.post(reverse('reset_password', kwargs={'uidb64': uidb64, 'token': token}), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('success', response.data)
