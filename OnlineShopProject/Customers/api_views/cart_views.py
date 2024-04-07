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
import logging

logger = logging.getLogger(__name__)

#shop
@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
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
    
#cart
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
class CartView(APIView):
    def get_cart(self, user):
        try:
            return Cart.objects.select_related('customer').get(customer=user)
        except Cart.DoesNotExist as err:
            logger.error(f'Cart not found for user {user.id}: {err}')
            raise

    def get(self, request): #showing cart content 3.4
        user = request.user
        try:
            cart = self.get_cart(user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post(self, request): #edit cart 3.2
        user = request.user
        product_id = request.data.get('product_id')
        new_quantity = request.data.get('new_quantity', None)
        remove_entire_item = request.data.get('remove_entire_item', False)

        try:
            cart = self.get_cart(user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            if remove_entire_item:
                cart_item.delete()
            elif new_quantity is not None:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return Response({'error': 'No edit parameters provided'}, status=status.HTTP_400_BAD_REQUEST)

            cart.refresh_from_db()
            serializer = CartSerializer(cart)
            return Response({'success': 'Cart updated', 'cart': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            logger.error(f'Error updating cart for user {user.id}: {e}')
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)