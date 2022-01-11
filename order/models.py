import secrets
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

def uuid_without_dash():
    return uuid.uuid4().hex


class Order(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    transaction_id = models.CharField(max_length=150)
    date_created = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__()

    def save(self, *args, **kwargs):
        transaction = self.transaction_id
        if (transaction is None) or (transaction == ""):
            self.transaction_id = secrets.token_hex(50)

        return super().save(*args, **kwargs)

