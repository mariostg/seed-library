from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from project.models import Order
from project.utils import send_donation_thank_you_email, send_order_confirmation_email


@shared_task
def send_order_confirmation_task(order_id):
    try:
        order = Order.objects.select_related("customer").get(id=order_id)
    except ObjectDoesNotExist:
        return False
    return send_order_confirmation_email(order)


@shared_task
def send_donation_thank_you_task(order_id):
    try:
        order = Order.objects.select_related("customer").get(id=order_id)
    except ObjectDoesNotExist:
        return False
    return send_donation_thank_you_email(order)
