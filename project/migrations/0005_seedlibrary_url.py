# Generated by Django 5.1.3 on 2024-11-15 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_seedlibrary_bloom_end_seedlibrary_bloom_start"),
    ]

    operations = [
        migrations.AddField(
            model_name="seedlibrary",
            name="url",
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
