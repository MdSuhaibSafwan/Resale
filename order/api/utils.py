from ..models import Order


def place_order_to_product(product_obj, user):
    Order.objects.create(product=product_obj, user=user)
