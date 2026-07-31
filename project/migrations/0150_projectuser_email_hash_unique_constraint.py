from django.db import migrations, models


def assert_projectuser_email_hash_unique(apps, schema_editor):
    ProjectUser = apps.get_model("project", "ProjectUser")

    duplicates = (
        ProjectUser.objects.exclude(email_hash="")
        .values("email_hash")
        .annotate(count=models.Count("id"))
        .filter(count__gt=1)
    )

    if duplicates.exists():
        sample = list(duplicates.values_list("email_hash", flat=True)[:5])
        raise RuntimeError(
            "Cannot add unique constraint on projectuser.email_hash: duplicate hashes found. "
            f"Sample hashes: {sample}"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0149_remove_customer_email"),
    ]

    operations = [
        migrations.RunPython(
            assert_projectuser_email_hash_unique,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="projectuser",
            constraint=models.UniqueConstraint(
                fields=("email_hash",),
                condition=~models.Q(email_hash=""),
                name="projectuser_email_hash_unique_nonempty",
            ),
        ),
    ]
