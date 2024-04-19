from rest_framework import serializers
from .models import Product, Category, DiscountCodes, Comment, ProductColor, ProductPicture

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'category', 'manufator_date']

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



class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = ('image',)

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('color',)

class ProducteDetailSerializer(serializers.ModelSerializer):
    pictures = ProductPictureSerializer(many=True, read_only=True)
    colors = serializers.SerializerMethodField()

    def get_colors(self, obj):
        colors = ProductColor.objects.filter(product=obj)
        return [color.color.color for color in colors]

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'category', 'price', 'manufator_date', 'detail', 'pictures', 'colors')