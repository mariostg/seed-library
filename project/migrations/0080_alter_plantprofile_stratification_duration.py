# Generated by Django 5.1.3 on 2024-12-12 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0079_alter_plantprofile_min_height"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plantprofile",
            name="stratification_duration",
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]