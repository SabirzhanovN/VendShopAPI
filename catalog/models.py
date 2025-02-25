from django.db import models
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='Price'
    )
    stock_house = models.PositiveIntegerField(default=1, verbose_name='StockHouse')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def clean(self):
        if self.price <= 0.0:
            raise ValidationError({'price': 'The price cannot be negative or equal to zero'})
