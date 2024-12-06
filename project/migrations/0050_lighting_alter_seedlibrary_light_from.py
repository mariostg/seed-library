# Generated by Django 5.1.3 on 2024-11-23 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0049_seedlibrary_container_suitable_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lighting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("lighting", models.CharField(max_length=45)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="seedlibrary",
            name="light_from",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.lighting"
            ),
        ),
    ]
