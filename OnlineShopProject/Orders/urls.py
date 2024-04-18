from django.urls import path

from .views import checkoutpage

urlpatterns = [
    # path('request/', send_request, name='request'),
    # path('verify/', verify , name='verify'),
    path('checkout/', checkoutpage, name='checkout')
]
