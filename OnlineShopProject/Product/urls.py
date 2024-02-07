from django.urls import path
from .views import list_categories,search_products

urlpatterns = [
    path('categories/', list_categories, name='categories-list'),
    path('products/search/', search_products, name='product-search'),
]