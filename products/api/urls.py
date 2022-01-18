from django.urls import path
from . import views

urlpatterns = [
    path("product/list-create/", views.ProductListCreateAPIView.as_view(), ),
    path("product/retrieve/<product_slug>/", views.ProductDetailAPIView.as_view(), ),
    path("product/<product_slug>/images/list-create/",  views.ProductImageListCreateAPIView.as_view(), ),
    path("user/bookmarks/", views.UserBookmarkAPIView.as_view(), ),

    path("todays-pick/list-create/", views.TodaysPickListCreateAPIView.as_view(), ),
    path("todays-pick/detail/<slug>/", views.TodaysPickRetrieveUpdateDestroyAPIView.as_view(), ),
]

