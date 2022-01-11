from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ProductListCreateSerializer, ProductRetrieveSerializer, ProductImageListCreateSerializer, ProductImageDetailSerializer
from ..models import Product, ProductImage, TodaysPick, BookMark, Category
from . import pagination, permissions
from rest_framework.views import APIView

from .utils import get_products_by_category, search_product

from django.contrib.auth import get_user_model

User = get_user_model()


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductListCreateSerializer
    pagination_class = pagination.Results20SetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        qs = Product.objects.all()
        qs = self.filter_through_name(qs)
        qs = self.filter_through_category(qs)
        return qs

    def filter_through_name(self, qs):
        name = self.request.query_params.get("name")
        if name is not None:
            qs = search_product(name, qs)

        return qs      

    def filter_through_category(self, qs):
        category = self.request.query_params.get("category")
        if category is not None:
            qs = get_products_by_category(category, qs)

        return qs

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductRetrieveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsProductOfCurrentUser]
    lookup_url_kwarg = "product_slug"

    def get_queryset(self):
        return None

    def get_object(self):
        product = self.get_product()
        return product

    def get_product(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            obj = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("Product with this Slug is not Found")

        return obj


class ProductImageListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductImageListCreateSerializer
    pagination_class = pagination.Results20SetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    lookup_url_kwarg = "product_slug"

    def get_queryset(self):
        product = self.get_product()
        qs = product.images.all().order_by("-last_updated")
        return qs

    def get_product(self):
        request = self.request
        slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            obj = Product.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("Product with this Slug is not Found")

        if request.method != "GET":
            if request.user != obj.user:
                raise PermissionDenied(f"User not permitted for {request.method} method")


        return obj

    def perform_create(self, serializer):
        product = self.get_product()
        if self.request.user != product.user:
            raise PermissionDenied("User is not permitted to add image")

        serializer.save(product=product)

    


class ProductImageDetailAPIView(RetrieveUpdateDestroyAPIView):
    pass


class UserBookmarkAPIView(APIView):
    pass
