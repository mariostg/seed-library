# Generated by Django 5.1.3 on 2024-11-16 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0011_sharingpriority_seedlibrary_sharing_priority"),
    ]

    operations = [
        migrations.AddField(
            model_name="seedlibrary",
            name="haresting_end",
            field=models.SmallIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name="seedlibrary",
            name="haresting_start",
            field=models.SmallIntegerField(blank=True, default=0),
        ),
    ]
