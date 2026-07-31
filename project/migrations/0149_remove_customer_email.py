from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0148_backfill_encrypted_email_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="email",
        ),
    ]
