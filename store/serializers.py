from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
