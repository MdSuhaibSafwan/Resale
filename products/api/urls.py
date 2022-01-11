from django.urls import path
from . import views

urlpatterns = [
    path("product/list-create/", views.ProductListCreateAPIView.as_view(), ),
    path("product/retrieve/<product_slug>/", views.ProductDetailAPIView.as_view(), ),
    path("product/<product_slug>/images/list-create/",  views.ProductImageListCreateAPIView.as_view(), ),
]

