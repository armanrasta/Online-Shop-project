from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product,Category,DiscountCodes,Comment
from .serializers import ProductSerializer,CategorySerializer,DiscountSerializer,CommentSerializer

# Create your views here.

@api_view(['GET'])
def list_categories(request):
    if request.method == "GET":
        categories = Category.objects.prefetch_related('subcat').all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])    
def category_management(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search_products(request):
    query_params = request.query_params
    name_contains = query_params.get('name_contains')
    brand_contains = query_params.get('brand_contains')
    min_price = query_params.get('min_price')
    max_price = query_params.get('max_price')

    products = Product.objects.all()
    
    if name_contains:
        products = products.filter(name__icontains=name_contains)
    
    if brand_contains:
        products = products.filter(brand__icontains=brand_contains)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def discount_codes_list(request):
    if request.method == 'GET':
        discount_codes = DiscountCodes.objects.all()
        serializer = DiscountSerializer(discount_codes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def discount_codes_detail(request, pk):
    try:
        discount_code = DiscountCodes.objects.get(pk=pk)
    except DiscountCodes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiscountSerializer(discount_code)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DiscountSerializer(discount_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        discount_code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
