import pytest
from django.test import Client


@pytest.mark.django_db
class TestPostAddPlantProfile:
    @pytest.fixture
    def setup(self):
        self.data = {
            "english_name": "",
            "french_name": "",
            "latin_name": "",
            "url": "",
            "bloom_start": "",
            "bloom_end": "",
            "min_height": "",
            "max_height": "",
            "stratification_detail": "",
            "stratification_duration": "",
            "sowing_depth": "",
            "sowing_period": "",
            "sharing_priority": "",
            "harvesting_start": "",
            "harvesting_indicator": "",
            "harvesting_mean": "",
            "seed_head": "",
            "remove_non_seed_material": "",
            "viability_test": "",
            "seed_storage": "",
            "one_cultivar": "",
            "packaging_measure": "",
            "dormancy": "",
            "seed_preparation": "",
            "hyperlink": "",
            "envelope_label_link": "",
            "harvesting_video_link": "",
            "seed_picture_link": "",
            "pods_seed_head_picture_link": "",
            "seed_storage_label_info": "",
            "notes": "",
            "germinate_easy": "",
            "rock_garden": "",
            "rain_garden": "",
            "pond_edge": "",
            "shoreline_rehab": "",
            "container_suitable": "",
            "ground_cover": "",
            "garden_edge": "",
            "woodland_garden": "",
            "wind_break_hedge": "",
            "erosion_control": "",
            "seed_availability": "",
            "keystones_species": "",
            "drought_tolerant": "",
            "salt_tolerant": "",
            "deer_tolerant": "",
            "easy_to_contain": "",
            "bloom_color": "",
            "habit": "",
        }

    def test_submit_form(self, setup):
        c = Client()
        response = c.post("/plant-profile-add/", self.data)
        assert 200 == response.status_code

    def test_submit_duplicate_latin_name_form(self, setup):
        c = Client()
        self.data["latin_name"] = "Dominus Sacapus"
        response = c.post("/plant-profile-add/", self.data)
        assert 200 == response.status_code
        response = c.post("/plant-profile-add/", self.data)
        assert "Plant profile with this Latin name already exists" in str(response.content)
