import django.db.models.deletion
from django.db import migrations, models


def copy_order_application_to_customer(apps, schema_editor):
    Order = apps.get_model("project", "Order")
    Customer = apps.get_model("project", "Customer")

    orders = Order.objects.exclude(application__isnull=True).select_related(
        "customer", "application"
    )
    for order in orders:
        customer = order.customer
        if customer and customer.application_id is None:
            Customer.objects.filter(pk=customer.pk, application__isnull=True).update(
                application_id=order.application_id
            )


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0133_remove_order_notes_order_customer_note"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="customers",
                to="project.orderseedapplication",
                verbose_name="Order Application",
            ),
        ),
        migrations.RunPython(
            copy_order_application_to_customer, migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name="order",
            name="application",
        ),
    ]
