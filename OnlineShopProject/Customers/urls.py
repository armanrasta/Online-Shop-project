from django.urls import path
from .views import address_page,login,login_otp,signup,sigup_otp

urlpatterns = [
    path('dashboard/address/', address_page, name='adress_page'),
    path('login/', login, name='login'),
    path('login-otp/', login_otp, name='login_otp'),
    path('signup/', signup, name='signup'),
    path('signup-otp/', sigup_otp, name='signup_otp')
]
