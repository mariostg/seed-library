from django import forms
from django.forms import ModelForm
from project import models
from django.core.exceptions import ValidationError
from django.utils.dates import MONTHS


class PlantProfileForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile

        fields = [
            "english_name",  #
            "french_name",  #
            "latin_name",  #
            "url",  #
            "light_from",  #
            "light_to",  #
            "bloom_start",  #
            "bloom_end",  #
            "soil_humidity_min",  #
            "soil_humidity_max",  #
            "min_height",  #
            "max_height",  #
            "stratification_detail",  #
            "stratification_duration",  #
            "sowing_depth",  #
            "sowing_period",
            "sharing_priority",  #
            "harvesting_start",  #
            "harvesting_end",  #
            "harvesting_indicator",  #
            "harvesting_mean",  #
            "seed_head",  #
            "remove_non_seed_material",  #
            "viability_test",  #
            "seed_storage",  #
            "one_cultivar",  #
            "packaging_measure",  #
            "dormancy",  #
            "seed_preparation",  #
            "hyperlink",  #
            "envelope_label_link",  #
            "harvesting_video_link",  #
            "seed_picture_link",  #
            "pods_seed_head_picture_link",  #
            "seed_storage_label_info",  #
            "notes",  #
            "germinate_easy",  #
            "rock_garden",  #
            "rain_garden",  #
            "pond_edge",  #
            "shoreline_rehab",  #
            "container_suitable",  #
            "ground_cover",  #
            "garden_edge",  #
            "woodland_garden",  #
            "wind_break_hedge",  #
            "erosion_control",  #
            "seed_availability",  #
            "keystones_species",  #
            "draught_tolerent",  #
            "salt_tolerent",  #
            "deer_tolerent",  #
            "easy_to_contain",  #
            "flower_color",
            "habit",  #
        ]

    def __init__(self, *args, **kwargs):
        super(PlantProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.required = False

    def clean(self):
        cleaned_data = super().clean()
        min_height = cleaned_data.get("min_height")
        max_height = cleaned_data.get("max_height")
        if min_height and max_height and min_height > max_height:
            raise ValidationError(
                f"Minimum height ({min_height}) must be smaller than maximum height ({max_height})"
            )

        bloom_start = cleaned_data.get("bloom_start")
        bloom_end = cleaned_data.get("bloom_end")
        if bloom_end and bloom_start and bloom_start > bloom_end:
            raise ValidationError(
                f"Beginning of blooming period ({ MONTHS[bloom_start]}) must be before end of blooming period ({MONTHS[bloom_end]})"
            )


class SearchPlantForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile

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


class ColorForm(forms.ModelForm):
    class Meta:
        model = models.Color
        fields = ["color"]

    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)


class DormancyForm(forms.ModelForm):
    class Meta:
        model = models.Dormancy
        fields = ["dormancy"]

    def __init__(self, *args, **kwargs):
        super(DormancyForm, self).__init__(*args, **kwargs)


class HabitForm(forms.ModelForm):
    class Meta:
        model = models.Habit
        fields = ["habit"]

    def __init__(self, *args, **kwargs):
        super(HabitForm, self).__init__(*args, **kwargs)


class HarvestingIndicatorForm(forms.ModelForm):
    class Meta:
        model = models.HarvestingIndicator
        fields = ["harvesting_indicator"]

    def __init__(self, *args, **kwargs):
        super(HarvestingIndicatorForm, self).__init__(*args, **kwargs)


class HarvestingMeanForm(forms.ModelForm):
    class Meta:
        model = models.HarvestingMean
        fields = ["harvesting_mean"]

    def __init__(self, *args, **kwargs):
        super(HarvestingMeanForm, self).__init__(*args, **kwargs)


class ProjectUserForm(ModelForm):
    class Meta:
        model = models.ProjectUser
        fields = ["name", "email"]

    def __init__(self, *args, **kwargs):
        super(ProjectUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
