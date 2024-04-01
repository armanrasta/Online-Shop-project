from django.urls import path
from .api_views import list_categories,search_products,ProductList,ProductDetail

urlpatterns = [
    path('categories/', list_categories, name='categories-list'),
    path('search/', search_products, name='search_products'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]