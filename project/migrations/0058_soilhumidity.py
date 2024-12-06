# Generated by Django 5.1.3 on 2024-11-26 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0057_seedlibrary_light_to_alter_seedlibrary_light_from"),
    ]

    operations = [
        migrations.CreateModel(
            name="SoilHumidity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("soil_humidity", models.CharField(blank=True, max_length=45)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
