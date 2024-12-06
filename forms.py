from django import forms
from django.forms import ModelForm
from project.models import SeedHarvesting


class SearchPlantForm(forms.ModelForm):
    class Meta:
        model = SeedHarvesting

        fields = [
            "english_name",
            "french_name",
            "latin_name",
            "Donate",
            "sharing_priority",
            "harvest_start",
            "harvest_end",
        ]

    def __init__(self, *args, **kwargs):
        super(SearchPlantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.required = False
