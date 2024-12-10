# Generated by Django 5.1.3 on 2024-12-10 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0074_sowingdepth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seedlibrary",
            name="sowing_depth",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="project.sowingdepth"
            ),
        ),
    ]
