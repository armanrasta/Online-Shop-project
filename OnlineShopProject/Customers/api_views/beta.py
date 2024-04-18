from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F
from ..models import Cart, CartItem
from Product.models import Product
from ..serializers import CartSerializer
import json
import logging

logger = logging.getLogger(__name__)
#cookie cart
def get_cookie_cart(request):
    cookie_cart = request.COOKIES.get('cookie_cart', '[]')
    return json.loads(cookie_cart)

def set_cookie_cart(response, cookie_cart):
    response.set_cookie('cookie_cart', json.dumps(cookie_cart), max_age=86400)
    
#show cart and edit the current cart items
class CartView(APIView):

    def get_cart(self, user):
        try:
            return Cart.objects.select_related('customer').get(customer=user)
        except Cart.DoesNotExist as err:
            raise err

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            try:
                cart = self.get_cart(user)
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cookie_cart = request.COOKIES.get('cookie_cart', '[]')
            return Response(json.loads(cookie_cart), status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request): #edit cart 3.2
        if request.user.is_authenticated:
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
                    return Response(
                        {'error': 'No edit parameters provided'}, status=status.HTTP_400_BAD_REQUEST)

                cart.refresh_from_db()
                serializer = CartSerializer(cart)
                return Response(
                    {'success': 'Cart updated', 'cart': serializer.data}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                logger.error(f'Error updating cart for user {user.id}: {e}')
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            cookie_cart = json.loads(request.COOKIES.get('cookie_cart', '[]'))
            product_id = request.data.get('product_id')
            new_quantity = int(request.data.get('new_quantity', 1))
            remove_entire_item = request.data.get('remove_entire_item', 'false').lower() == 'true'
            price = request.data.get('price', '')
            brand = request.data.get('brand', '')
            manufacture_date = request.data.get('manufacture_date', '')
            name = request.data.get('name', '')

            if not product_id:
                return JsonResponse({'error': 'Product ID is missing'}, status=400)

            product_in_cart = next((item for item in cookie_cart if item['product_id'] == product_id), None)

            if product_in_cart:
                if remove_entire_item or product_in_cart['quantity'] <= 1:
                    cookie_cart = [item for item in cookie_cart if item['product_id'] != product_id]
                else:
                    product_in_cart['quantity'] = new_quantity
                    product_in_cart['brand'] = brand
                    product_in_cart['manufacture_date'] = manufacture_date
                    product_in_cart['name'] = name
            else:
                cookie_cart.append({
                    'product_id': product_id,
                    'name': name,
                    'quantity': new_quantity,
                    'price': price,
                    'brand': brand,
                    'manufacture_date': manufacture_date
                })
            response = JsonResponse({'success': 'Cart updated'})
            response.set_cookie('cookie_cart', json.dumps(cookie_cart), max_age=86400)
            return response

#add products
@api_view(['POST'])
def add_to_cart(request):
    authenticated = request.user.is_authenticated
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    if not product_id:
        return JsonResponse({'error': 'Product ID is missing'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if authenticated:
        user = request.user

        if quantity < 1:
            return Response({'error': 'Quantity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                cart, _ = Cart.objects.get_or_create(customer=user)
                
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                if not created:
                    cart_item.quantity = F('quantity') + quantity
                    cart_item.save()
                else:
                    cart_item.quantity = quantity
                    cart_item.save()

                cart.refresh_from_db()
                serializer = CartSerializer(cart)
                return Response({'success': 'Item added to cart', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Error adding product to cart: {e}')
            return Response({'error': 'Error adding item to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        cookie_cart = get_cookie_cart(request)
        
        product_exists = any(item['product_id'] == product_id for item in cookie_cart)

        if product_exists:
            for item in cookie_cart:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    break
        else:
            cookie_cart.append({'product_id': product_id, 'quantity': quantity})

        response = JsonResponse({'success': 'Item added to cookie cart'})
        set_cookie_cart(response, cookie_cart)
        return response