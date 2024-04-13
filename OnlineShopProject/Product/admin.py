from django.contrib import admin
from .models import Category, Product, DiscountCodes, Comment, ProductPicture, ProductColor
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(DiscountCodes)
admin.site.register(Comment)
admin.site.register(ProductPicture)
admin.site.register(ProductColor)