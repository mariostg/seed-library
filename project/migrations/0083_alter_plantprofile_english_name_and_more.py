# Generated by Django 5.1.3 on 2024-12-12 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0082_alter_plantprofile_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plantprofile",
            name="english_name",
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name="plantprofile",
            name="french_name",
            field=models.CharField(blank=True, max_length=75),
        ),
    ]
