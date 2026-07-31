from django.db import migrations


def backfill_encrypted_email_fields(apps, schema_editor):
    from project.email_security import email_hash, encrypt_email

    Customer = apps.get_model("project", "Customer")
    ProjectUser = apps.get_model("project", "ProjectUser")

    for customer in Customer.objects.all().only("id", "email"):
        Customer.objects.filter(id=customer.id).update(
            email_encrypted=encrypt_email(customer.email),
            email_hash=email_hash(customer.email),
        )

    for user in ProjectUser.objects.all().only("id", "email"):
        ProjectUser.objects.filter(id=user.id).update(
            email_encrypted=encrypt_email(user.email),
            email_hash=email_hash(user.email),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0147_add_encrypted_email_fields"),
    ]

    operations = [
        migrations.RunPython(
            backfill_encrypted_email_fields,
            migrations.RunPython.noop,
        ),
    ]
