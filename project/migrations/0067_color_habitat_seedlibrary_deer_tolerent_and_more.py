# Generated by Django 5.1.3 on 2024-12-08 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0066_seedlibrary_seed_availability"),
    ]

    operations = [
        migrations.CreateModel(
            name="Color",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("color", models.CharField(blank=True, max_length=25)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Habitat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("habitat", models.CharField(blank=True, max_length=30)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="deer_tolerent",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="draught_tolerent",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="easy_to_contain",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="keystones_species",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="salt_tolerent",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="flower_color",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.color"
            ),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="habitat",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.habitat"
            ),
        ),
    ]
