from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
import random
from string import ascii_letters

User = get_user_model()

def create_random_slug(num=10):
    return "".join(random.choice(ascii_letters) for i in range(num))


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


def category_in_tuple():
    qs = Category.objects.all()
    cat = []
    for i in qs:
        cat.append((i.title, i.title))

    cat = tuple(cat)
    return cat


class Product(models.Model):
    CATEGORY = category_in_tuple()
    PRODUCT_STATUS = (
        ("ON-SELL", "ON-SELL"),
        ("ORDERED", "ORDERED"),
        ("BOUGHT", "BOUGHT"),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=500)
    price = models.FloatField()
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=500, choices=CATEGORY)
    status = models.CharField(max_length=15, choices=PRODUCT_STATUS, default="ON-SELL")
    city = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.name) + create_random_slug()

        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="images")
    image = models.ImageField(upload_to="product_images")
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.product.name) + "|image-" + create_random_slug()

        return super().save(*args, **kwargs)        


class TodaysPick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    date_created = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.product.name) + "|today-pick" + create_random_slug()

        return super().save(*args, **kwargs)        

    def is_product_of_today(self):
        date = self.date_created
        time_now = timezone.now()
        return time_now.date() == date


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    date_created = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  

    class Meta:
        unique_together = ["user", "product"]

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.product.name) + "|bookmark" + create_random_slug()

        return super().save(*args, **kwargs)      

    def __str__(self):
        return self.product.name
