from django.urls import path
from .api_views import customer_auth
from .api_views.beta import CartView, add_to_cart 
from .api_views.address import AddressListCreateView, AddressRetrieveUpdateView

urlpatterns = [
    path('signup/', customer_auth.create_account, name='signup'),
    path('signup-otp/', customer_auth.signup_otp, name='signup_otp'),
    path('login-otp/', customer_auth.login_otp, name='login_otp'),
    path('login/', customer_auth.login, name='login'),
    path('cart/', CartView.as_view(), name = 'cart_detail'),
    path('add_to_cart/', add_to_cart, name = 'add to cart'),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateView.as_view(), name='address-retrieve-update'),
]