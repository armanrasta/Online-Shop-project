from django.urls import path
from .views import address_page

urlpatterns = [
    path('address/', address_page, name='adress_page'),
]
