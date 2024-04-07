from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from ..models import Cart, CartItem, Product
from ..serializers import CartItemSerializer, CartSerializer

#shop
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

        cart.refresh_from_db()
        serializer = CartSerializer(cart)
        return Response(
            {'success': 'Item added to cart', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
#cart
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
class CartView(APIView):
    def get(self, request): #show cart
        user = request.user
        try:
            cart = Cart.objects.get(customer=user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request): #edit cart
        user = request.user
        product_id = request.data.get('product_id')
        new_quantity = request.data.get('new_quantity', None)
        remove_entire_item = request.data.get('remove_entire_item', False)

        try:
            cart = Cart.objects.get(customer=user)
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
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)