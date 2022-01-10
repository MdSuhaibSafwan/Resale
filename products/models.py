from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)

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
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=500)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=500, choices=CATEGORY)
    city = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="images")
    image = models.ImageField(upload_to="product_images")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product.name




