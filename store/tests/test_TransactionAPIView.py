from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalog.models import Product
from django.db import transaction


class TransactionAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product1 = Product.objects.create(name='Product 1', price=10.0, stock_house=5)
        cls.product2 = Product.objects.create(name='Product 2', price=20.0, stock_house=0)

        cls.client = APIClient()

    def test_successful_transaction(self):
        """
        Successful transaction test (product in stock and enough money)
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': self.product1.id,
            'count': 2,
            'balance': 50.0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'OK')
        self.assertEqual(response.data['change'], 30.0)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock_house, 3)

    def test_product_not_found(self):
        """
        Test if product does not exist
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': 999,
            'count': 1,
            'balance': 50.0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No such product')

    def test_not_enough_stock(self):
        """
        Test if there is not enough product in stock
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': self.product2.id,
            'count': 10,
            'balance': 100.0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Product is out of stock!')

    def test_not_enough_money(self):
        """
        Test if you don't have enough money to buy
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': self.product1.id,
            'count': 2,
            'balance': 19
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Тot enough money!')

    def test_invalid_product_id(self):
        """
        Test for incorrect product_id (non-numeric or missing)
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': 'invalid_id',
            'count': 2,
            'balance': 50.0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_count(self):
        """
        Test for incorrect quantity of products
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': self.product1.id,
            'count': -2,
            'balance': 50.0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_balance(self):
        """
        Test for incorrect balance (not a number or negative value)
        """
        url = '/api/store/transaction/'
        data = {
            'product_id': self.product1.id,
            'count': 2,
            'balance': -123
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_atomic(self):
        """
        Finally test transaction
                :)
        """
        url = '/api/store/transaction/'
        initial_balance = self.product1.stock_house
        data = {
            'product_id': self.product1.id,
            'count': 2,
            'balance': 100.0
        }

        with transaction.atomic():
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.product1.refresh_from_db()
            self.assertEqual(self.product1.stock_house, initial_balance - 2)
