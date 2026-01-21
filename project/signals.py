"""
Django signals for the project app.
Automatically sends emails when orders are created.
This module is imported in the ready() method of ProjectConfig in apps.py.
It is not really used anymore since we moved email sending to Celery tasks,
but kept here for reference.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """
    Signal handler to send order confirmation email when an Order is created.

    Args:
        sender: The model class (Order)
        instance: The actual instance being saved (the Order object)
        created: Boolean, True if the instance was just created
        **kwargs: Additional keyword arguments
    """
    if created:
        logger.info(
            "Order created: #%s by %s %s -- signal no longer sends emails",
            instance.id,
            instance.customer.first_name,
            instance.customer.last_name,
        )
