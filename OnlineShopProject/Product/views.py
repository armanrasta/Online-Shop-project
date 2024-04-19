from django.shortcuts import render

# Create your views here.

def shop_category(request, category_name):
    return render(request, 'Product/shop.html', {'category_name': category_name})

def product_detail(request, product_id):
    return render(request, 'Product/detail.html', {'product_id': product_id})

def index_page(request):
    return render(request, 'Product/index.html')