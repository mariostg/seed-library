# Generated by Django 5.1.3 on 2024-12-08 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0069_soilhumidity_definition"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Habitat",
            new_name="Habit",
        ),
        migrations.RenameField(
            model_name="habit",
            old_name="habitat",
            new_name="habit",
        ),
        migrations.RenameField(
            model_name="seedlibrary",
            old_name="habitat",
            new_name="habit",
        ),
    ]
