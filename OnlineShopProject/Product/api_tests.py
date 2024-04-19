from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Customers.models import Customer
from .models import Product, Category, DiscountCodes, Comment
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer, CommentSerializer

class CategoryTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', is_subcat=False)

    def test_list_categories(self):
        url = reverse('list-categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_detail(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_create_category(self):
        url = reverse('category-list-create')
        data = {'name': 'New Category', 'is_subcat': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  

    def test_delete_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0) 

class ProductTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', brand='Test Brand', quantity=10,
                                              category=Category.objects.create(name='Test Category', is_subcat=False),
                                              price=100, manufator_date='2023-01-01')

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'New Product', 'brand': 'New Brand', 'quantity': 20, 'category': self.category.pk, 'price': 200, 'manufator_date': '2023-02-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0) 


class DiscountCodesTests(APITestCase):
    pass

class CommentTests(APITestCase):
    def setUp(self):
        self.Customer = Customer.objects.create(first_name='John', last_name='Doe', username='johndoe', phone_number='1234567890', email='john@example.com', password='testpassword')
        self.product = Product.objects.create(name='Test Product', brand='Test Brand', quantity=10, price=100, manufator_date='2023-01-01')
        self.comment = Comment.objects.create(product=self.product, User=self.Customer, Comment='Test comment', rating=5)

    def test_comment_list(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_comment_detail(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Comment'], 'Test comment')

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'product': self.product.pk, 'User': self.Customer.pk, 'Comment': 'New comment', 'rating': 4}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)  # Check if a new comment is created

    def test_delete_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)