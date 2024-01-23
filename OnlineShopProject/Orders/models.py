from django.db import models
from Costumers.models import Costumer
from Product.models import Product, DiscountCodes

# Create your models here.

class Order(models.Model):
    
    class PaymentChoices(models.TextChoices):
        Online = "OL", ("Online")
        OnDoor = "OD", ("OnDoor")
        
    class StatusChoices(models.TextChoices):
        Canceled = "C", ("Cancelled")
        Done = "D", ("Delivered")
        InProgress = "I", ("IN progress")
    
    costumer = models.ForeignKey(Costumer, on_delete = models.CASCADE)
    discount = models.ForeignKey(DiscountCodes, on_delete = models.DO_NOTHING)
    total_price = models.DecimalField(null = True, decimal_places = 3, max_digits = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    description = models.TextField(null = True)
    status = models.CharField(choices = StatusChoices, default = StatusChoices.InProgress, max_length = 30)
    
    def __str__(self):
        return f'{str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = total - self.discount
            return discount_price
        return total
    
    
class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    quantity = models.IntegerField(default = 1)
    
    def get_cost(self):
        return self.item.price * self.quantity
    