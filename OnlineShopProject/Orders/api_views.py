from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Product, Transaction
from Customers.models import Cart

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def cart_to_order(request):
    with transaction.atomic():
        # Assume user and cart are already retrieved from the request
        user = request.user
        cart = Cart.objects.get(customer=user)

        # Create the order
        order = Order.objects.create(customer=user, status=Order.StatusChoices.InProgress)

        # Add items from the cart to the order
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order, item=cart_item.product, quantity=cart_item.quantity)
            # Update product stock
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

        cart.delete()

        return Response({'success': 'Order finalized and payment processed'})