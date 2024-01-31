from django.test import TestCase
from datetime import date
from Costumers.models import Costumer
from Product.models import Product, DiscountCodes
from .models import Order, OrderItem, Transaction

class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Costumer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number='12345678901',
            email='johndoe@example.com',
            password='hashed_password'
        )

        self.discount_code = DiscountCodes.objects.create(
            code='DISCOUNT10',
            discount_type='P',
            discount=10
        )

        self.product = Product.objects.create(
            name='Smartphone',
            brand='Samsung',
            quantity=10,
            category=None,
            price=500,
            manufator_date=date(2022, 1, 1),
            pic='static/img/smartphone.jpg'
        )

        self.order_item = OrderItem.objects.create(
            order=None,
            item=self.product,
            quantity=2
        )

        self.order = Order.objects.create(
            amount=0,
            customer=self.customer,
            discount=self.discount_code,
            total_price=0,
            description='Test Order',
            status='I'
        )
        self.order.items.add(self.order_item)

    def test_order_str_method(self):
        expected_str = f'{str(self.order.id)}'
        self.assertEqual(str(self.order), expected_str)

    def test_order_save_method(self):
        self.order.save()
        self.assertEqual(self.order.amount, 1000)  # Assuming the product price is 500 and quantity is 2
        self.assertEqual(self.order.total_price, 900)  # Assuming a 10% discount

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.customer = Costumer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number='12345678901',
            email='johndoe@example.com',
            password='hashed_password'
        )

        self.discount_code = DiscountCodes.objects.create(
            code='DISCOUNT10',
            discount_type='P',
            discount=10
        )

        self.product = Product.objects.create(
            name='Smartphone',
            brand='Samsung',
            quantity=10,
            category=None,
            price=500,
            manufator_date=date(2022, 1, 1),
            pic='static/img/smartphone.jpg'
        )

        self.order_item = OrderItem.objects.create(
            order=None,
            item=self.product,
            quantity=2
        )

    def test_order_item_str_method(self):
        expected_str = f'{self.product.brand} - {self.product.name}'
        self.assertEqual(str(self.order_item), expected_str)

    def test_order_item_get_cost_method(self):
        cost = self.order_item.get_cost()
        self.assertEqual(cost, 1000)  # Assuming the product price is 500 and quantity is 2

class TransactionModelTest(TestCase):

    def setUp(self):
        self.customer = Costumer.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            phone_number='12345678901',
            email='johndoe@example.com',
            password='hashed_password'
        )

        self.discount_code = DiscountCodes.objects.create(
            code='DISCOUNT10',
            discount_type='P',
            discount=10
        )

        self.product = Product.objects.create(
            name='Smartphone',
            brand='Samsung',
            quantity=10,
            category=None,
            price=500,
            manufator_date=date(2022, 1, 1),
            pic='static/img/smartphone.jpg'
        )

        self.order_item = OrderItem.objects.create(
            order=None,
            item=self.product,
            quantity=2
        )

        self.order = Order.objects.create(
            amount=0,
            customer=self.customer,
            discount=self.discount_code,
            total_price=0,
            description='Test Order',
            status='I'
        )
        self.order.items.add(self.order_item)

        self.transaction = Transaction.objects.create(
            amount=0,
            currency='R',
            payment_method='CA',
            order=self.order,
            customer=self.customer,
            description='Test Transaction',
            refund_amount=0,
            refund_reason=None
        )

    def test_transaction_str_method(self):
        self.assertIsNotNone(str(self.transaction))
