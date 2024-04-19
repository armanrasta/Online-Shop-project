from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber
from .models import Customer, Address

class CustomerModelTest(TestCase):

    def setUp(self):
        self.Customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number=PhoneNumber.from_string('+12345678901'),
            email='johndoe@example.com',
            password='hashed_password'
        )

    def test_Customer_str_method(self):
        self.assertEqual(str(self.Customer), 'johndoe')

class AddressModelTest(TestCase):

    def setUp(self):
        self.Customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number=PhoneNumber.from_string('+12345678901'),
            email='johndoe@example.com',
            password='hashed_password'
        )

        self.address = Address.objects.create(
            Customer=self.Customer,
            state='California',
            city='Los Angeles',
            full_address='123 Main St',
            lat=34.0522,
            lon=-118.2437,
            postal_code=90001,
            extra_description='Apartment 456'
        )

    def test_address_str_method(self):
        expected_str = f"{self.address.id} - {self.Customer}"
        self.assertEqual(str(self.address), expected_str)
