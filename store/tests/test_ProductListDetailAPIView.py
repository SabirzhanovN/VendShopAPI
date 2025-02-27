from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from catalog.models import Product

class ProductListDetailAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product1 = Product.objects.create(name='Product 1', price=10.0, stock_house=1)
        cls.product2 = Product.objects.create(name='Product 2', price=20.0, stock_house=0)
        cls.product3 = Product.objects.create(name='Product 3', price=30.0, stock_house=1)
        cls.product4 = Product.objects.create(name='Product 4', price=40.0, stock_house=0)
        cls.product5 = Product.objects.create(name='Product 5', price=50.0, stock_house=1)
        cls.client = APIClient()

    def test_list_products(self):
        url = '/api/store/products/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_products_available(self):
        url = '/api/store/products/?stock_house=available'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_products_unavailable(self):
        url = '/api/store/products/?stock_house=unavailable'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_products_empty_stock_house(self):
        url = '/api/store/products/?stock_house='
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve_product(self):
        url = f'/api/store/products/{self.product1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_retrieve_product_not_found(self):
        url = '/api/store/products/1111111/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
