import pytest

from project import models
from project.forms import (
    ColorForm,
    DormancyForm,
    HabitForm,
    HarvestingIndicatorForm,
    HarvestingMeanForm,
    PlantCollectionForm,
    PlantProfileForm,
    ProjectUserForm,
    SearchPlantForm,
)


@pytest.mark.django_db
class TestForms:
    @pytest.fixture
    def plant_profile_data(self):
        models.GrowthHabit.objects.create(habit="Habiter")
        models.FlowerColor.objects.create(color="Red")
        models.SeedStorage.objects.create(seed_storage="Storage")
        models.SeedStorageLabelInfo.objects.create(seed_storage_label_info="Info")
        models.SeedPreparation.objects.create(seed_preparation="Preparation")
        models.Dormancy.objects.create(dormancy="Dormancy")
        models.HarvestingIndicator.objects.create(harvesting_indicator="Indicator")
        models.HarvestingMean.objects.create(harvesting_mean="Mean")
        models.Lighting.objects.create(lighting="Lighting 1")
        models.Lighting.objects.create(lighting="Lighting 2")
        models.SoilHumidity.objects.create(soil_humidity="Humidity 1")
        models.SoilHumidity.objects.create(soil_humidity="Humidity 2")
        models.PackagingMeasure.objects.create(packaging_measure="Measure")
        models.OneCultivar.objects.create(one_cultivar="One cultivar")
        models.ViablityTest.objects.create(viability_test="Testme")
        models.SeedHead.objects.create(seed_head="Head")
        models.SharingPriority.objects.create(sharing_priority="Priority")
        models.SowingDepth.objects.create(sowing_depth="Depth")
        return {
            "english_name": "Rose",
            "french_name": "Rose",
            "latin_name": "Rosa",
            "url": "http://example.com",
            "bloom_start": 1,
            "bloom_end": 12,
            "soil_humidity_min": 1,
            "soil_humidity_max": 2,
            "min_height": 10,
            "max_height": 100,
            "stratification_detail": "Detail",
            "stratification_duration": 30,
            "sowing_depth": 1,
            "sowing_period": "Spring",
            "sharing_priority": 1,
            "harvesting_start": 1,
            "harvesting_indicator": 1,
            "harvesting_mean": 1,
            "seed_head": 1,
            "remove_non_seed_material": "Material",
            "viability_test": True,
            "seed_storage": 1,
            "one_cultivar": True,
            "packaging_measure": 1,
            "dormancy": 1,
            "seed_preparation": 1,
            "hyperlink": "http://example.com",
            "envelope_label_link": "http://example.com",
            "harvesting_video_link": "http://example.com",
            "seed_picture_link": "http://example.com",
            "pods_seed_head_picture_link": "http://example.com",
            "seed_storage_label_info": 1,
            "notes": "Notes",
            "germinate_easy": True,
            "rock_garden": True,
            "rain_garden": True,
            "pond_edge": True,
            "shoreline_rehab": True,
            "container_suitable": True,
            "ground_cover": True,
            "garden_edge": True,
            "woodland_garden": True,
            "wind_break_hedge": True,
            "erosion_control": True,
            "seed_availability": True,
            "keystones_species": True,
            "drought_tolerant": True,
            "salt_tolerant": True,
            "deer_tolerant": True,
            "easy_to_contain": True,
            "flower_color": 1,
            "habit": 1,
        }

    def test_plant_profile_form_valid(self, plant_profile_data):
        form = PlantProfileForm(data=plant_profile_data)

        assert form.is_valid()

    def test_plant_profile_form_invalid_height(self, plant_profile_data):
        plant_profile_data["min_height"] = 200
        form = PlantProfileForm(data=plant_profile_data)
        assert not form.is_valid()
        assert "Minimum height (200) must be smaller than maximum height (100)" in str(form.errors)

    def test_plant_profile_form_invalid_bloom(self, plant_profile_data):
        plant_profile_data["bloom_start"] = 12
        plant_profile_data["bloom_end"] = 1
        form = PlantProfileForm(data=plant_profile_data)
        assert not form.is_valid()
        assert "Beginning of blooming period (December) must be before end of blooming period (January)" in str(
            form.errors
        )

    def test_search_plant_form_valid(self):
        models.SoilHumidity.objects.create(soil_humidity="Humidity 1")
        models.Lighting.objects.create(lighting="Lighting 1")
        models.Lighting.objects.create(lighting="Lighting 2")
        models.SoilHumidity.objects.create(soil_humidity="Humidity 1")
        models.SoilHumidity.objects.create(soil_humidity="Humidity 2")
        models.SharingPriority.objects.create(sharing_priority="Priority")

        data = {
            "english_name": "Rose",
            "french_name": "Rose",
            "latin_name": "Rosa",
            "bloom_start": 1,
            "bloom_end": 12,
            "soil_humidity_min": 1,
            "soil_humidity_max": 2,
            "max_height": 100,
            "stratification_duration": 30,
            "sharing_priority": 1,
            "harvesting_start": 1,
            "germinate_easy": True,
            "seed_availability": True,
        }
        form = SearchPlantForm(data=data)
        assert form.is_valid()

    def test_color_form_valid(self):
        data = {"color": "Red"}
        form = ColorForm(data=data)
        assert form.is_valid()

    def test_dormancy_form_valid(self):
        data = {"dormancy": "Dormant"}
        form = DormancyForm(data=data)
        assert form.is_valid()

    def test_habit_form_valid(self):
        data = {"habit": "Habit"}
        form = HabitForm(data=data)
        assert form.is_valid()

    def test_harvesting_indicator_form_valid(self):
        data = {"harvesting_indicator": "Indicator"}
        form = HarvestingIndicatorForm(data=data)
        assert form.is_valid()

    def test_harvesting_mean_form_valid(self):
        data = {"harvesting_mean": "Mean"}
        form = HarvestingMeanForm(data=data)
        assert form.is_valid()

    def test_project_user_form_valid(self):
        data = {"username": "user", "email": "user@example.com"}
        form = ProjectUserForm(data=data)
        assert form.is_valid()

    def test_plant_collection_form_valid(self):
        data = {"details": "Details"}
        form = PlantCollectionForm(data=data)
        assert form.is_valid()
