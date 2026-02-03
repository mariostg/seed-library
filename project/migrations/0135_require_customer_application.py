import django.db.models.deletion
from django.db import migrations, models


def ensure_customer_application(apps, schema_editor):
    OrderSeedApplication = apps.get_model("project", "OrderSeedApplication")
    Customer = apps.get_model("project", "Customer")

    default_application = OrderSeedApplication.objects.order_by(
        "priority", "seed_application"
    ).first()
    if default_application is None:
        default_application = OrderSeedApplication.objects.create(
            seed_application="Unspecified",
            priority=0,
        )

    Customer.objects.filter(application__isnull=True).update(
        application_id=default_application.id
    )


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0134_move_order_application_to_customer"),
    ]

    operations = [
        migrations.RunPython(ensure_customer_application, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="customer",
            name="application",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="customers",
                to="project.orderseedapplication",
                verbose_name="Order Application",
            ),
        ),
    ]
