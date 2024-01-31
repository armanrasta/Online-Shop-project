from django.db import models
from Costumers.models import Costumer

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    is_subcat = models.BooleanField(default=False)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcat', limit_choices_to={'is_subcat': False})
    pic = models.ImageField(upload_to= "static/img")
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    
    name = models.CharField(max_length = 30)
    brand = models.CharField(max_length = 30)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, limit_choices_to={'is_subcat': True}, verbose_name="Selected Subcategory", on_delete=models.CASCADE)
    price = models.IntegerField()
    manufator_date = models.DateField()
    pic = models.ImageField(upload_to= "static/img")
    
    def __str__(self):
        return f"{self.brand} - {self.name}"
    
class DiscountCodes(models.Model):
    
    code = models.TextField(max_length = 16 , unique = True)
    discount_type = models.CharField(max_length=10, choices = [('P', 'Percent'), ('F', 'Fixed')], null = True, blank = True)
    discount = models.IntegerField(max_length = 100000000)
    
    def __str__(self):
        return self.code
    
class Comment(models.Model):
    
    rating_choices = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    User = models.ForeignKey(Costumer, on_delete=models.DO_NOTHING)
    Comment = models.TextField(max_length = 2000)
    rating = models.IntegerField(choices = rating_choices)