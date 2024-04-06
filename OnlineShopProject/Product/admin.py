from django.contrib import admin
from .models import Category, Product, DiscountCodes, Comment, ProductPicture
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(DiscountCodes)
admin.site.register(Comment)
admin.site.register(ProductPicture)