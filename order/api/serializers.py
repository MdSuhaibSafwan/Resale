from re import T
from ..models import Order
from products.models import Product
from products.api import serializers as ProductSerializer

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class OrderSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)
    transaction_id = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = "__all__"
