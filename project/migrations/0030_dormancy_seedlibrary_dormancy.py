# Generated by Django 5.1.3 on 2024-11-20 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0029_alter_seedstorage_seed_storage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dormancy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("dormancy", models.CharField(blank=True, max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="dormancy",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.dormancy"
            ),
        ),
    ]
