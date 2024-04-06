from django.urls import path
from .api_views import customer_auth

urlpatterns = [
    path('signup/', customer_auth.signup_otp, name='signup'),
    path('sigup-otp/', customer_auth.create_account, name='signup_otp'),
    path('login-otp/', customer_auth.login_otp, name='login_otp'),
    path('login/', customer_auth.login, name='login'),
]