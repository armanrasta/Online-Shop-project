from rest_framework import serializers
from .models import Cart, CartItem, Customer

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items']
        
class CustomerCartSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = []

    def get_cart(self, obj):
        try:
            cart = Cart.objects.get(customer=obj)
            serializer = CartSerializer(cart)
            return serializer.data
        except Cart.DoesNotExist:
            return None