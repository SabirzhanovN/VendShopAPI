from rest_framework import viewsets, mixins

from catalog.serializers import ProductSerializer
from catalog.models import Product

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

