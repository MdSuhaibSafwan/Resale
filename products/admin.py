from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Product, ProductImage, TodaysPick, Category

User = get_user_model()


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(TodaysPick)
admin.site.register(Category)
