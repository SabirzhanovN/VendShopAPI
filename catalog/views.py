from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import ProductSerializer
from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    """
    For only admin users to CRUD products.

    PUT, PATCH, DELETE, POST available only via pk.
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    queryset = Product.objects.all()


