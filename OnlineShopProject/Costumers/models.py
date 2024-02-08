from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from Product.models import Product
class Costumer(models.Model):
    
    user = models.OneToOneField(User,blank = True, null = True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(null=False, blank=False, unique=True, max_length = 32)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, max_length = 11)
    email = models.EmailField(null=False, blank=False, unique=True, max_length=254)
    password = models.CharField(null=False,max_length = 1000)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    
    
    def __str__(self):
        return self.username
    
class Address(models.Model):
    
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    state = models.CharField(null=False, blank=False, max_length = 30)
    city = models.CharField(null=False, blank=False, max_length = 30)
    full_address = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    postal_code = models.IntegerField(max_length = 10)
    extra_description = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.costumer}"

class Cart(models.Model):
    customer = models.OneToOneField(Costumer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.customer.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart of {self.cart.customer.username}"