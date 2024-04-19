from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from ..models import Cart, CartItem, Product
from ..serializers import CartItemSerializer, CartSerializer
from Customers.permissions import IsCustomer
import logging

logger = logging.getLogger(__name__)

#shop
@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated, IsCustomer])
def add_to_cart(request): #3.2
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not isinstance(quantity, int) or quantity < 1:
        return Response(
            {'error': 'Quantity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            product = Product.objects.get(id=product_id)
            cart, _ = Cart.objects.get_or_create(customer=user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
            cart_item.save()

            cart.refresh_from_db()
            serializer = CartSerializer(cart)
            return Response(
                {'success': 'Item added to cart', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        logger.error(f'Product with id {product_id} does not exist.')
        return Response(
            {'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error adding product to cart: {e}')
        return Response(
            {'error': 'Error adding item to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)