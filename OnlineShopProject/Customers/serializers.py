from rest_framework import serializers
from .models import Cart, CartItem, Customer,Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
        extra_kwargs = {
            'username': {'read_only': True}
        }
        
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product_name', 'product_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'items']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())

class CustomerCartSerializer(serializers.ModelSerializer): #un necesarry
    cart = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['cart']

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
        fields = ['state', 'city', 'full_address', 'postal_code', 'extra_description']
        
    def create(self, validated_data):
        validated_data['Customer'] = self.context['request'].user
        return Address.objects.create(**validated_data)