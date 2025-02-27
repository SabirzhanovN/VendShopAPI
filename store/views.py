from django.db import transaction
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response

from catalog.serializers import ProductSerializer
from catalog.models import Product

from .serializers import TransactionSerializer

class ProductListDetailAPIView(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    """
    View only for listing and detail(via pk) Product.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        """
        Ability to filter products by availability.

            .../?stock_house=
            .../?stock_house=available
            .../?stock_house=unavailable
        """
        queryset = Product.objects.all()
        stock_house = self.request.query_params.get('stock_house')

        if stock_house == 'available':
            queryset = Product.objects.filter(stock_house__gt = 0)

        if stock_house == 'unavailable':
            queryset = Product.objects.filter(stock_house=0)

        return queryset


class TransactionAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        count = serializer.validated_data['count']
        balance = serializer.validated_data['balance']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'No such product'}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock_house < count:
            return Response({'error': 'Product is out of stock!'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = product.price * count
        if balance < total_price:
            return Response({'error': 'Тot enough money!'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            change = balance - total_price

            product.stock_house -= count
            product.save()

        return Response({'message': 'OK', 'change': change}, status=status.HTTP_201_CREATED)


