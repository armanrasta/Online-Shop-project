from django.urls import path
from . import api_views

urlpatterns = [
    path('signup/', api_views.signup_otp, name='signup'),
    path('verify-otp/', api_views.create_account, name='verify_otp'),
    path('login-otp/', api_views.login_otp, name='login_otp'),
    path('login/', api_views.login, name='login'),
]