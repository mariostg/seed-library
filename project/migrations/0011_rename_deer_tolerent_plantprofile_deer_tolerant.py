# Generated by Django 5.1.3 on 2025-01-15 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0010_rename_salt_tolerent_plantprofile_salt_tolerant"),
    ]

    operations = [
        migrations.RenameField(
            model_name="plantprofile",
            old_name="deer_tolerent",
            new_name="deer_tolerant",
        ),
    ]
