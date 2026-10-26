import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0154_customer_accept_substitutes"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="donor_address",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="donation",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="donations",
                to="project.order",
            ),
        ),
    ]
