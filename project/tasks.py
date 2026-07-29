from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Count, Sum
from django.utils import timezone

from project.filters import OrderFilter
from project.models import Order
from project.utils import (
    render_many_orders_to_pdf,
    send_donation_thank_you_email,
    send_order_confirmation_email,
)

GENERATED_ORDERS_PDF_DIR = "generated/filtered-orders"
DEFAULT_ORDERS_PDF_RETENTION_DAYS = 7


def _iter_storage_files(storage, root_dir):
    """Yield file paths under ``root_dir`` recursively for storages supporting listdir."""
    try:
        directories, files = storage.listdir(root_dir)
    except Exception:
        return

    for name in files:
        yield f"{root_dir}/{name}"

    for directory in directories:
        child_dir = f"{root_dir}/{directory}"
        yield from _iter_storage_files(storage, child_dir)


def cleanup_generated_orders_pdfs(retention_days=None):
    """Delete old generated order PDFs from storage.

    Args:
        retention_days: Number of days to keep files. If ``None``, uses
            ``settings.ORDERS_PDF_RETENTION_DAYS`` or falls back to
            ``settings.PENDING_ORDERS_PDF_RETENTION_DAYS`` for backward compatibility.

    Returns:
        int: Number of deleted files.
    """
    if retention_days is None:
        retention_days = getattr(
            settings,
            "ORDERS_PDF_RETENTION_DAYS",
            getattr(
                settings,
                "PENDING_ORDERS_PDF_RETENTION_DAYS",
                DEFAULT_ORDERS_PDF_RETENTION_DAYS,
            ),
        )

    retention_days = max(int(retention_days), 0)
    cutoff = timezone.now() - timedelta(days=retention_days)
    deleted_count = 0

    for file_path in _iter_storage_files(default_storage, GENERATED_ORDERS_PDF_DIR):
        try:
            modified = default_storage.get_modified_time(file_path)
        except Exception:
            continue

        if modified < cutoff:
            default_storage.delete(file_path)
            deleted_count += 1

    return deleted_count


def _build_filtered_orders_queryset(filter_params):
    orders = (
        Order.objects.select_related("customer")
        .prefetch_related("items__plant_profile")
        .annotate(
            orderitem_count=Count("items", distinct=True),
            total_seed_quantity=Sum("items__quantity"),
        )
        .order_by("-order_date")
    )

    pdf_status = filter_params.get("pdf_status")
    if pdf_status == "printed":
        orders = orders.filter(pdf_generated_at__isnull=False)
    elif pdf_status == "not_printed":
        orders = orders.filter(pdf_generated_at__isnull=True)

    order_filter = OrderFilter(filter_params, queryset=orders)
    return order_filter.qs


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


@shared_task(bind=True)
def generate_filtered_orders_pdf_task(
    self, filter_params=None, generated_by_user_id=None
):
    """Build a filtered-orders PDF in the background and save it to storage."""
    cleanup_generated_orders_pdfs()

    filter_params = filter_params or {}
    orders = _build_filtered_orders_queryset(filter_params)

    generated_by_user = None
    if generated_by_user_id is not None:
        User = get_user_model()
        try:
            generated_by_user = User.objects.get(id=generated_by_user_id)
        except User.DoesNotExist:
            pass

    pdf = render_many_orders_to_pdf(orders, generated_by=generated_by_user)
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    file_name = (
        f"{GENERATED_ORDERS_PDF_DIR}/filtered_orders_{timestamp}_{self.request.id}.pdf"
    )

    return default_storage.save(file_name, ContentFile(pdf))


@shared_task
def cleanup_generated_orders_pdfs_task(retention_days=None):
    """Celery task wrapper for generated order PDF cleanup."""
    return cleanup_generated_orders_pdfs(retention_days=retention_days)
