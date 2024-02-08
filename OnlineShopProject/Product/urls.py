from django.urls import path
from .views import list_categories,search_products,ProductList,ProductDetail

urlpatterns = [
    path('categories/', list_categories, name='categories-list'),
    path('products/search/', search_products, name='product-search'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]