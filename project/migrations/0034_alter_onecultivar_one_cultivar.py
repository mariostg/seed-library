# Generated by Django 5.1.3 on 2024-11-21 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0033_seedlibrary_seed_preparation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onecultivar",
            name="one_cultivar",
            field=models.CharField(blank=True, max_length=125),
        ),
    ]
