from rest_framework import serializers
from .models import Cart, CartItem, Customer,Address

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
        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['state', 'city', 'full_address', 'lat', 'lon', 'postal_code', 'extra_description']
        
    def create(self, validated_data):
        validated_data['Customer'] = self.context['request'].user
        return Address.objects.create(**validated_data)