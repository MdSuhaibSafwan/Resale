from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from ..models import Product, ProductImage, TodaysPick, BookMark

User = get_user_model()


class ProductListCreateSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    status = serializers.CharField(read_only=True)
    front_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_front_image(self, serializer):
        try:
            image_obj = serializer.images.order_by("-last_updated")[0]
        except IndexError:
            return None
        
        image_url = image_obj.image.url
        if "http" not in image_url:
            request = self.context.get("request")
            http = request.get_raw_uri().split(request.get_host())[0]
            raw_path = http + request.get_host()
            image_url = raw_path + image_url
        return image_url


class ProductImageListCreateSerializer(ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductImageDetailSerializer(ModelSerializer):
    product = ProductListCreateSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductRetrieveSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    status = serializers.CharField(read_only=True)
    images = ProductImageListCreateSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"


class BookMarkSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = ProductListCreateSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = BookMark
        fields = "__all__"


class TodaysPickSerializer(ModelSerializer):
    product = ProductListCreateSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = TodaysPick
        fields = "__all__"

    def get_is_valid(self, serializer):
        return serializer.picked_till_date >= timezone.now()

    def validate_picked_till_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Provide a time greater than today")
        return value

