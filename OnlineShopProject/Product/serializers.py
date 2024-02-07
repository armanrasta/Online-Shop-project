from rest_framework import serializers
from .models import Product, Category, DiscountCodes

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        
class DiscountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DiscountCodes
        fields = '__all__'