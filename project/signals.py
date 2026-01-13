"""
Django signals for the project app.
Automatically sends emails when orders are created.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from project import utils
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
        logger.info("Order created: #%s by %s", instance.id, instance.customer.name)

        # Send order confirmation email
        try:
            success = utils.send_order_confirmation_email(instance)
            if success:
                logger.info(
                    "Order confirmation email sent successfully for Order #%s to %s",
                    instance.id,
                    instance.customer.email,
                )
            else:
                logger.error(
                    "Failed to send order confirmation email for Order #%s",
                    instance.id,
                )
        except Exception as e:
            logger.exception(
                "Error sending order confirmation email for Order #%s: %s",
                instance.id,
                e,
            )

        # Send donation thank you email if donation was made
        if instance.donation_amount and instance.donation_amount > 0:
            logger.info(
                "Processing donation of $%s for Order #%s",
                instance.donation_amount,
                instance.id,
            )
            try:
                success = utils.send_donation_thank_you_email(instance)
                if success:
                    logger.info(
                        "Donation thank you email sent successfully for Order #%s (Amount: $%s)",
                        instance.id,
                        instance.donation_amount,
                    )
                else:
                    logger.error(
                        "Failed to send donation thank you email for Order #%s",
                        instance.id,
                    )
            except Exception as e:
                logger.exception(
                    "Error sending donation thank you email for Order #%s: %s",
                    instance.id,
                    e,
                )
