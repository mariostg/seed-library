# Generated by Django 5.1.3 on 2024-12-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0068_lighting_definition"),
    ]

    operations = [
        migrations.AddField(
            model_name="soilhumidity",
            name="definition",
            field=models.CharField(blank=True, max_length=75),
        ),
    ]
