from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from project import models
from project.management.commands.create_dummy_orders import (
    DEBUG_CUSTOMER_EMAIL_PREFIX,
    DEBUG_ORDER_NOTE,
)


class Command(BaseCommand):
    help = "Delete only debug-generated orders created by create_dummy_orders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many records would be deleted without deleting them.",
        )
        parser.add_argument(
            "--delete-debug-customers",
            action="store_true",
            help="Also delete debug customers that no longer have orders.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        delete_debug_customers = options["delete_debug_customers"]

        debug_orders = models.Order.objects.filter(
            Q(customer_note=DEBUG_ORDER_NOTE)
            | Q(customer__email__startswith=DEBUG_CUSTOMER_EMAIL_PREFIX)
        )

        debug_order_ids = list(debug_orders.values_list("id", flat=True))
        debug_customer_ids = list(
            debug_orders.values_list("customer_id", flat=True).distinct()
        )

        items_count = models.OrderItem.objects.filter(
            order_id__in=debug_order_ids
        ).count()
        orders_count = len(debug_order_ids)

        self.stdout.write(
            f"Matched debug data: {orders_count} orders, {items_count} order items."
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run: no records deleted."))
            return

        deleted_items, _ = models.OrderItem.objects.filter(
            order_id__in=debug_order_ids
        ).delete()
        deleted_orders, _ = models.Order.objects.filter(id__in=debug_order_ids).delete()

        deleted_customers = 0
        if delete_debug_customers and debug_customer_ids:
            customers_qs = models.Customer.objects.filter(
                id__in=debug_customer_ids,
                email__startswith=DEBUG_CUSTOMER_EMAIL_PREFIX,
                orders__isnull=True,
            )
            deleted_customers, _ = customers_qs.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Deleted debug data: "
                f"orders={deleted_orders}, order_items={deleted_items}, "
                f"customers={deleted_customers}."
            )
        )
