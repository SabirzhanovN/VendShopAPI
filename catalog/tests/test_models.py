from django.test import TestCase
from django.core.exceptions import ValidationError

from catalog.models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name='Cola', price=1.1, stock_house=2)
        self.assertEqual(product.name, 'Cola')
        self.assertEqual(product.price, 1.1)
        self.assertEqual(product.stock_house, 2)

    def test_product_str(self):
        product = Product.objects.create(name='Cola', price=1.1, stock_house=2)
        self.assertEqual(str(product), 'Cola')

    def test_price_cannot_be_negative(self):
        product = Product(name='Cola', price=-1, stock_house=2)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_price_cannot_be_zero(self):
        product = Product(name='Cola', price=0, stock_house=2)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_default_stock_house(self):
        product = Product.objects.create(name='Default Stock', price=1.1)
        self.assertEqual(product.stock_house, 1)
