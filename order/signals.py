from django.db.models.signals import post_save
from .models import Order, Product
from django.dispatch import receiver


@receiver(signal=post_save, sender=Order)
def change_product_status(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.status = Product.PRODUCT_STATUS[1][0]
        product.save()
        return True

    return False