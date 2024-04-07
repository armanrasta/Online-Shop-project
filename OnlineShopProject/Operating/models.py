from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Operators(AbstractUser):
    phone_number = PhoneNumberField(unique = True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='Operator_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this Operator belongs to. A Operator will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='operator_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this Customer.'
    )

    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'

    def __str__(self):
        return self.username