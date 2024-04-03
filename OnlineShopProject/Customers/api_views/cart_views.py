from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from ..models import Cart, CartItem, Product
from ..serializers import CartItemSerializer

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(customer=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({'success': 'Item added to cart'}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def show_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(customer=user)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_to_cookie_cart(request):
    if not request.user.is_authenticated:
        # Retrieve the current cart from the cookies or create a new one if it doesn't exist
        cookie_cart = request.COOKIES.get('cookie_cart', '[]')
        cookie_cart = json.loads(cookie_cart)

        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Check if the product is already in the cart and update the quantity
        product_exists = False
        for item in cookie_cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                product_exists = True
                break

        # If the product is not in the cart, add it
        if not product_exists:
            cookie_cart.append({'product_id': product_id, 'quantity': quantity})

        # Create a response and add the updated cart to the cookies
        response = JsonResponse({'success': 'Item added to cookie cart'})
        response.set_cookie('cookie_cart', json.dumps(cookie_cart), max_age=3600)  # Expires in 1 hour

        return response
    else:
        # If the user is authenticated, you might want to handle this differently
        return JsonResponse({'error': 'User is authenticated, use the database cart'}, status=400)

# Remember to replace 'product_id' and 'quantity' with the actual POST data keys you are using.