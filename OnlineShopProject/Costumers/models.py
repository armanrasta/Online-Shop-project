from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Costumer(models.Model):
    
    first_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, max_length = 11)
    email = models.EmailField(null=False, blank=False, unique=True, max_length=254)
    
    def __str__(self):
        return self.name
    
    
class Address(models.Model):
    
    state = models.CharField()
    city = models.CharField()
    