from django.db import models
from Costumers.models import Costumer
from Product.models import Product, DiscountCodes
import uuid
from core.models import BaseModel

class Order(BaseModel):
    class PaymentChoices(models.TextChoices):
        Online = "OL", ("Online")
        OnDoor = "OD", ("OnDoor")

    class StatusChoices(models.TextChoices):
        Refunded = "R", ("Refunded")
        Canceled = "C", ("Cancelled")
        Done = "D", ("Delivered")
        InProgress = "I", ("IN progress")

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountCodes, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(null=True, decimal_places=3, max_digits=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.InProgress, max_length=30)
    items = models.ManyToManyField("OrderItem", related_name='orders')

    def __str__(self):
        return f'{str(self.id)}'

    def save(self, *args, **kwargs):
        self.amount = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            if self.discount.type == 'F':
                self.total_price = self.amount - self.discount.amount
            elif self.discount.type == 'P':
                self.total_price = self.amount * (1 - self.discount.amount / 100)
        super().save(*args, **kwargs)
        
class OrderItem(BaseModel):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    add_date = models.DateTimeField(auto_now_add = True)
    
    def get_cost(self):
        return self.item.price * self.quantity

class Transaction(BaseModel):
    
    payment_method_choices = (
        ('CA', 'Cash'),
        ('CR', 'Credit'),
        ('DC', 'Debit Card')
    )
    currency_choices= (
        ('R' , 'Rial'),
        ('B' , 'BTC'),
        ('D' , 'DOllar')
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    # status = models.CharField(max_length=20)
    payment_method = models.CharField(choices = payment_method_choices)
    transaction_id = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    order = models.ForeignKey(Order, on_delete = models.DO_NOTHING)
    customer = models.ForeignKey(Costumer, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.amount = self.order.amount
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.transaction_id
    