from django.urls import path
from .api_views import list_categories,search_products,ProductList,ProductDetailView,products_by_category

urlpatterns = [
    path('categories/', list_categories, name='categories-list'),
    path('search/', search_products, name='search_products'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<str:category_name>/', products_by_category, name='products-by-category'),
]