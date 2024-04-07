from rest_framework import serializers
from .models import Product, Category, DiscountCodes, Comment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'price', 'category', 'manufator_date']

class CategorySerializer(serializers.ModelSerializer):
    subcats = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'subcats']

    def get_subcats(self, obj):
        if obj.is_subcat:
            return None
        else:
            child_categories = Category.objects.filter(parent_category=obj)
            serializer = CategorySerializer(child_categories, many=True)
            return serializer.data

class DiscountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DiscountCodes
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
