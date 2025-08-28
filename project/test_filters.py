from django.db.models import QuerySet
from django.test import TestCase

from project.filters import PlantProfileFilter
from project.models import PlantProfile


class TestPlantProfileFilter(TestCase):
    def setUp(self):
        self.filter = PlantProfileFilter()
        self.queryset = PlantProfile.objects.all()

    def test_filter_seed_availability_true(self):
        # Test when value is True
        filtered = self.filter.filter_seed_availability(
            self.queryset, "seed_availability", True
        )
        self.assertIsInstance(filtered, QuerySet)
        self.assertEqual(
            str(filtered.query), str(self.queryset.filter(seed_availability=True).query)
        )

    def test_filter_seed_availability_false(self):
        # Test when value is False
        filtered = self.filter.filter_seed_availability(
            self.queryset, "seed_availability", False
        )
        self.assertIsInstance(filtered, QuerySet)
        self.assertEqual(
            str(filtered.query),
            str(self.queryset.exclude(seed_availability=True).query),
        )
