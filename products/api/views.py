from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ProductSerializer, ProductImageListCreateSerializer, ProductImageDetailSerializer
from ..models import Product, ProductImage, TodaysPick, BookMark, Category
from . import pagination, permissions
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

User = get_user_model()


class ProductListCreateAPIView(ListCreateAPIView):
    pass


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    pass


class ProductImageListCreateAPIView(ListCreateAPIView):
    pass


class ProductImageDetailAPIView(RetrieveUpdateDestroyAPIView):
    pass


class UserBookmarkAPIView(APIView):
    pass
