from django import forms
from django.forms import ModelForm
from project.models import SeedLibrary


class SearchPlantForm(forms.ModelForm):
    class Meta:
        model = SeedLibrary

        fields = [
            "english_name",
            "french_name",
            "latin_name",
            "light_from",
            "light_to",
            "bloom_start",
            "bloom_end",
            "soil_humidity_min",
            "soil_humidity_max",
            "max_height",
            "stratification_duration",
            "sharing_priority",
            "harvesting_start",
            "harvesting_end",
            "germinate_easy",
            "seed_availability",
        ]

    def __init__(self, *args, **kwargs):
        super(SearchPlantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.required = False
