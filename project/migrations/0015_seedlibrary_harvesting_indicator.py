# Generated by Django 5.1.3 on 2024-11-18 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0014_harvestingindicator"),
    ]

    operations = [
        migrations.AddField(
            model_name="seedlibrary",
            name="harvesting_indicator",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.harvestingindicator"
            ),
        ),
    ]
