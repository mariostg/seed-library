# Generated by Django 5.1.3 on 2024-12-31 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_alter_plantmorphology_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sharingpriority",
            name="level",
            field=models.CharField(
                blank=True,
                choices=[("none", "None"), ("low", "Low"), ("medium", "Medium"), ("high", "High")],
                default="None",
                max_length=10,
            ),
        ),
    ]
