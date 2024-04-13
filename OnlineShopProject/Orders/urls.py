# Github.com/Rasooll
from django.urls import path
from .zarinpal import send_request

urlpatterns = [
    path('request/', send_request, name='request'),
    # path('verify/', verify , name='verify'),
]
