from django.test import Client, TestCase
from django.urls import reverse

from project.models import PlantProfile


class SearchPlantNameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.plant1 = PlantProfile.objects.create(latin_name="Abies balsamea", seed_availability=True)
        self.plant2 = PlantProfile.objects.create(latin_name="Betula papyrifera")
        self.search_url = reverse("search-plant-name")

    def test_empty_search_returns_no_results(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
        self.assertTemplateUsed(response, "project/plant-catalog.html")

    def test_search_returns_correct_plant(self):
        response = self.client.get(self.search_url + "?seed_availability=available-seed")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        plant = response.context["object_list"][0]
        self.assertEqual(plant.latin_name, "Abies balsamea")

    def test_search_returns_all_plants_ordered(self):
        response = self.client.get(self.search_url + "?any_name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 2)
        plants = list(response.context["object_list"])
        self.assertEqual(plants[0].latin_name, "Abies balsamea")
        self.assertEqual(plants[1].latin_name, "Betula papyrifera")

    def test_htmx_request_uses_different_template(self):
        response = self.client.get(self.search_url, headers={"hx-request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/plant-search-results.html")

    def test_context_contains_required_data(self):
        response = self.client.get(self.search_url)
        self.assertIn("search_filter", response.context)
        self.assertIn("object_list", response.context)
        self.assertEqual(response.context["url_name"], "index")
        self.assertEqual(response.context["title"], "Plant Profile Filter")
