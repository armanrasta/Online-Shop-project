from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    is_subcat = models.BooleanField(default=False)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcat', limit_choices_to={'is_subcat': False})

    def __str__(self):
        return self.name
    
class Product(models.Model):
    
    name = models.CharField(max_length = 30)
    brand = models.CharField(max_length = 30)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, limit_choices_to={'is_subcat': True}, verbose_name="Selected Subcategory", on_delete=models.CASCADE)
    price = models.IntegerField()
    manufator_date = models.DateField()
    
    def __str__(self):
        return f"{self.brand} - {self.name}"
    
class DiscountCodes(models.Model):
    
    code = models.TextField(max_length = 16 , unique = True)
    discount = models.IntegerField(max_length = 100000000)
    
    def __str__(self):
        return self.code