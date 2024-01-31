from django.test import TestCase
from datetime import date
from Costumers.models import Costumer
from .models import Category, Product, DiscountCodes, Comment

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            is_subcat=False,
            pic='static/img/electronics.jpg'
        )

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Electronics')

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            is_subcat=False,
            pic='static/img/electronics.jpg'
        )

        self.product = Product.objects.create(
            name='Smartphone',
            brand='Samsung',
            quantity=10,
            category=self.category,
            price=500,
            manufator_date=date(2022, 1, 1),
            pic='static/img/smartphone.jpg'
        )

    def test_product_str_method(self):
        expected_str = 'Samsung - Smartphone'
        self.assertEqual(str(self.product), expected_str)

class DiscountCodesModelTest(TestCase):

    def setUp(self):
        self.discount_code = DiscountCodes.objects.create(
            code='DISCOUNT10',
            discount_type='P',
            discount=10
        )

    def test_discount_codes_str_method(self):
        self.assertEqual(str(self.discount_code), 'DISCOUNT10')

class CommentModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            is_subcat=False,
            pic='static/img/electronics.jpg'
        )

        self.product = Product.objects.create(
            name='Smartphone',
            brand='Samsung',
            quantity=10,
            category=self.category,
            price=500,
            manufator_date=date(2022, 1, 1),
            pic='static/img/smartphone.jpg'
        )

        self.customer = Costumer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number='12345678901',
            email='johndoe@example.com',
            password='hashed_password'
        )

        self.comment = Comment.objects.create(
            product=self.product,
            User=self.customer,
            Comment='This is a great product!',
            rating=5
        )

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'This is a great product!')
