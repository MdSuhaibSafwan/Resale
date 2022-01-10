from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Category, ProductImage, Product, TodaysPick
from django.utils import timezone


def get_products_by_category(title):
    try:
        category = Category.objects.get(title=title)
    except ObjectDoesNotExist:
        raise NotFound("Category with this name is not found.")

    qs = Product.objects.filter(category=category.title)
    return qs


def get_product(slug):
    try:
        obj = Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise NotFound("Product with this slug is not found.")

    return obj


def search_product(name):
    qs = Product.objects.filter(name=name)
    return qs


def get_product_images(product_obj):
    images_qs = product_obj.images.all()
    return images_qs
    

def get_product_image(slug):
    try:
        obj = ProductImage.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise NotFound("Image with this slug is not found.")

    return obj


def get_todays_pick():
    time_now = timezone.now().date()
    qs = TodaysPick.objects.filter(date_created=time_now)
    return qs

