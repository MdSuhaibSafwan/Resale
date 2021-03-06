from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from ..models import Category, ProductImage, Product, TodaysPick
from django.utils import timezone


def get_products_by_category(title, qs=None):
    try:
        category = Category.objects.get(title=title)
    except ObjectDoesNotExist:
        raise NotFound("Category with this name is not found.")
    if qs is not None:
        qs = qs.filter(category=category.title)
        return qs

    qs = Product.objects.filter(category=category.title)
    return qs


def get_product(slug):
    try:
        obj = Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise NotFound("Product with this slug is not found.")

    return obj


def search_product(name, qs=None):
    if qs is not None:
        qs = qs.filter(name=name)
        return qs
        
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


def get_todays_pick_in_accordance_to_time():
    time_now = timezone.now()
    qs = TodaysPick.objects.filter(picked_till_date__gt=time_now)
    return qs
