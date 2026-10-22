from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0152_orderscanimportaudit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="stripe_invoice_id",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
