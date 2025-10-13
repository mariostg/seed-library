from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.dates import MONTHS

from project import models


class PlantProfileForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile

        fields = [
            "english_name",  #
            "french_name",  #
            "latin_name",  #
            "bloom_start",  #
            "bloom_end",  #
            "max_height",  #
            "stratification_detail",  #
            "stratification_duration",  #
            "sowing_depth",  #
            "harvesting_start",  #
            "harvesting_indicator",  #
            "harvesting_mean",  #
            "seed_head",  #
            "remove_non_seed_material",  #
            "seed_viability_test",  #
            "seed_storage",  #
            "on_cultivar",  #
            "packaging_measure",  #
            "seed_preparation",  #
            "envelope_label_link",  #
            "harvesting_video_link",  #
            "seed_storage_label_info",  #
            "notes",  #
            "germinate_easy",  #
            "rock_garden",  #
            "rain_garden",  #
            "shoreline_rehab",  #
            "container_suitable",  #
            "ground_cover",  #
            "woodland_garden",  #
            "seed_availability",  #
            "keystones_species",  #
            "drought_tolerant",  #
            "salt_tolerant",  #
            "deer_tolerant",  #
            "easy_to_contain",  #
            "bloom_colour",
            "growth_habit",  #
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.required = False

    def clean(self):
        cleaned_data = super().clean()
        min_height = cleaned_data.get("min_height")
        max_height = cleaned_data.get("max_height")
        latin_name = cleaned_data.get("latin_name")
        if min_height and max_height and min_height > max_height:
            raise ValidationError(
                f"{latin_name}: Minimum height ({min_height}) must be smaller than maximum height ({max_height})"
            )

        bloom_start = cleaned_data.get("bloom_start")
        bloom_end = cleaned_data.get("bloom_end")
        if bloom_end and bloom_start and bloom_start > bloom_end:
            raise ValidationError(
                f"Beginning of blooming period ({ MONTHS[bloom_start]}) must be before end of blooming period ({MONTHS[bloom_end]})"
            )


class PlantProfileSearchForm(forms.Form):
    plant_name = forms.CharField(max_length=100)


class SearchPlantForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile

        fields = [
            "english_name",
            "french_name",
            "latin_name",
            "bloom_start",
            "bloom_end",
            "max_height",
            "stratification_duration",
            "harvesting_start",
            "germinate_easy",
            "seed_availability",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.required = False


class AdminColourForm(forms.ModelForm):
    class Meta:
        model = models.BloomColour
        fields = ["bloom_colour"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdminLifespanForm(forms.ModelForm):
    class Meta:
        model = models.PlantLifespan
        fields = ["lifespan", "definition"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EnvironmentalRequirementsForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "full_sun",
            "part_shade",
            "full_shade",
            "moisture_dry",
            "moisture_medium",
            "moisture_wet",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HabitForm(forms.ModelForm):
    class Meta:
        model = models.GrowthHabit
        fields = ["growth_habit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HarvestingIndicatorForm(forms.ModelForm):
    class Meta:
        model = models.HarvestingIndicator
        fields = ["harvesting_indicator"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HarvestingMeanForm(forms.ModelForm):
    class Meta:
        model = models.HarvestingMean
        fields = ["harvesting_mean"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProjectUserForm(ModelForm):
    class Meta:
        model = models.ProjectUser
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class PlantCollectionForm(forms.ModelForm):
    class Meta:
        model = models.PlantCollection
        fields = ["details"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantIdentificationInformationForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "is_draft",
            "is_active",
            "is_accepted",
            "not_accepted_reason",
            "has_notice",
            "notice_detail",
            "show_bees_supported_info",
            "show_butterflies_supported_info",
            "show_complementary_plants_info",
            "show_ecological_benefits_info",
            "show_ecozones_info",
            "show_env_requirements_info",
            "show_gardener_friendly_info",
            "show_harvesting_info",
            "show_inaturalist_link_info",
            "show_landscape_uses_info",
            "show_obsolete_names_info",
            "show_sowing_info",
            "show_tolerates_info",
            "show_vascan_map_info",
            "latin_name",
            "english_name",
            "french_name",
            "taxon",
            "inaturalist_taxon",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # latin_name required
        self.fields["latin_name"].required = True


class PlantGrowthCharacteristicsForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "bloom_start",
            "bloom_end",
            "bloom_colour",
            "max_height",
            "max_width",
            "lifespan",
            "spring_ephemeral",
            "growth_habit",
            "spread_by_rhizome",
            "does_not_spread",
            "dioecious",
            "germinate_easy",
            "self_seeding",
            "beginner_friendly",
            "transplantation_tolerant",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantLandscapeUseAndApplicationForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "pollinator_garden",
            "rock_garden",
            "rain_garden",
            "shoreline_rehab",
            "container_suitable",
            "school_garden",
            "ground_cover",
            "woodland_garden",
            "boulevard_garden_tolerant",
            "wetland_garden",
            "easy_to_contain",
            "hedge",
            "foot_traffic_tolerance_no",
            "foot_traffic_tolerance_light",
            "foot_traffic_tolerance_medium",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantEcologicalBenefitsForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "bees",
            "bee_host",
            "bird_friendly",
            "butterflies",
            "butterfly_host",
            "hummingbird_friendly",
            "keystones_species",
            "pollinator_garden",
            "deer_tolerant",
            "rabbit_tolerant",
            "drought_tolerant",
            "foot_traffic_tolerance_no",
            "foot_traffic_tolerance_light",
            "foot_traffic_tolerance_medium",
            "juglone_tolerant",
            "nitrogen_fixer",
            "salt_tolerant",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantSpecialFeaturesAndConsiderationForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "septic_tank_safe",
            "produces_burs",
            "cause_skin_rashes",
            "toxicity_indicator",
            "toxicity_indicator_notes",
            "alternative_to_notes",
            "grasp_candidate",
            "grasp_candidate_notes",
            "conservation_status",
            "native_to_ottawa_region",
            "ecozones",
            "is_native_to_AB",
            "is_native_to_BC",
            "is_native_to_MB",
            "is_native_to_NB",
            "is_native_to_NL",
            "is_native_to_NS",
            "is_native_to_ON",
            "is_native_to_PE",
            "is_native_to_QC",
            "is_native_to_SK",
            "is_native_to_YT",
            "is_native_to_NT",
            "is_native_to_NU",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantHarvestingForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "harvesting_start",
            "harvesting_indicator",
            "harvesting_mean",
            "seed_viability_test",
            "seed_head",
            "remove_non_seed_material",
            "seed_storage",
            "on_cultivar",
            "harvesting_video_link",
            "harvesting_notes",
        ]


class PlantSowingForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "sowing_depth",
            "stratification_detail",
            "stratification_duration",
            "double_dormancy",
            "sowing_notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantSeedDistributionForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "packaging_measure",
            "seed_preparation",
            "sowing_label_instructions",
            "sowing_notes",
            "envelope_label_link",
            "seed_storage_label_info",
            "seed_event_table",
            "notes",
            "accepting_seed",
            "seed_availability",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlantIntroductoryGardeningExperienceForm(forms.ModelForm):
    class Meta:
        model = models.PlantProfile
        fields = [
            "beginner_friendly",
            "does_not_spread",
            "germinate_easy",
            "self_seeding",
            "starter_pack_shade",
            "starter_pack_sun_dry",
            "starter_pack_sun_wet",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
