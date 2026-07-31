from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0146_remove_order_created_remove_order_modified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="email_encrypted",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="customer",
            name="email_hash",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=64
            ),
        ),
        migrations.AddField(
            model_name="projectuser",
            name="email_encrypted",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="projectuser",
            name="email_hash",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=64
            ),
        ),
    ]
