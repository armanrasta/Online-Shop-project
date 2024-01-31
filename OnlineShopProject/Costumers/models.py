from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Costumer(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(null=False, blank=False, unique=True, max_length = 32)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, max_length = 11)
    email = models.EmailField(null=False, blank=False, unique=True, max_length=254)
    password = models.CharField(null=False,max_length = 1000)
    
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