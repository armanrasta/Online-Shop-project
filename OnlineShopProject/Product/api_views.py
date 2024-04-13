from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product,Category,DiscountCodes,Comment
from .serializers import ProductSerializer,CategorySerializer,DiscountSerializer,CommentSerializer
from Customers.serializers import CartSerializer

#category
@api_view(['GET'])
def list_categories(request):
    parent_categories = Category.objects.filter(parent_category__isnull=True)
    serializer = CategorySerializer(parent_categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT','DELETE'])    
def category_management(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'POST' or 'PUT':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#product search and filtering
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

#product
@api_view(['GET'])
def products_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name, is_subcat=True)
    products = Product.objects.filter(category=category)
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(products, request)
    if page is not None:
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#discount
@api_view(['GET', 'POST', 'PUT'])
def discount_codes_list(request):
    if request.method == 'GET':
        discount_codes = DiscountCodes.objects.all()
        serializer = DiscountSerializer(discount_codes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST' or 'PUT':
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def discount_codes_detail(request, pk):
    try:
        discount_code = DiscountCodes.objects.get(pk=pk)
    except DiscountCodes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiscountSerializer(discount_code)
        return Response(serializer.data)

    elif request.method == 'POST' or 'PUT':
        serializer = DiscountSerializer(discount_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        discount_code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
####
class ApplyDiscount(APIView):
    def post(self, request):
        
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart = cart_serializer.validated_data
            discount_code = cart.get('discount_code')
            try:
                discount = DiscountCodes.objects.get(code=discount_code, availablity=True)
            except DiscountCodes.DoesNotExist:
                return Response({'error': 'Invalid or unavailable discount code'}, status=400)
            
            total_price = cart.get('total_price')
            if discount.discount_type == 'P':
                discount_amount = (total_price * discount.discount) / 100
                total_price -= discount_amount
            elif discount.discount_type == 'F':
                total_price -= discount.discount
            
            return Response({'total_price': total_price})
        return Response(cart_serializer.errors, status=400)

    
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(APIView):  #for admin panel
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#demo
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
