from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from ..models import Product, ProductImage,TodaysPick, BookMark

User = get_user_model()


class ProductSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductImageListCreateSerializer(ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductImageDetailSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = ProductImage
        fields = "__all__"
