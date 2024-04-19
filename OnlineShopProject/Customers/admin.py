from django.contrib import admin
from .models import Customer, Address, Cart, CartItem
# Register your models here.

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)