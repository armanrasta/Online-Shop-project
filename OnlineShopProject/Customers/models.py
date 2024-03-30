from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from Product.models import Product


class Customer(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    otp_code = models.CharField(max_length=6, null=True, blank=True, validators=[
                                MinLengthValidator(6)])

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this customer belongs to. A customer will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this customer.'
    )

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.username


class Address(models.Model):

    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField(null=False, blank=False, max_length=30)
    city = models.CharField(null=False, blank=False, max_length=30)
    full_address = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    postal_code = models.IntegerField(max_length=10)
    extra_description = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.Customer}"


class Cart(models.Model):

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart of {self.cart.customer.username}"
