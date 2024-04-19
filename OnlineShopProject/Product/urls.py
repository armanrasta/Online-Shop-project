from django.urls import path
from .views import shop_category, product_detail,index_page

urlpatterns = [
    path('shop/<str:category_name>/', shop_category, name='shop-category'),
    path('shop/detail/<int:product_id>/', product_detail, name='product_deatil'),
    path('', index_page, name='index_page'),
]
