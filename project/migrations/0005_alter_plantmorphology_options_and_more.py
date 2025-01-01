# Generated by Django 5.1.3 on 2024-12-28 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_plantmorphology"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="plantmorphology",
            options={"ordering": ["element"], "verbose_name_plural": "plant morphology"},
        ),
        migrations.AddField(
            model_name="plantimage",
            name="morphology_aspect",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="project.plantmorphology"
            ),
            preserve_default=False,
        ),
    ]