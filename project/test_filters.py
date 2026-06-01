from django.db.models import QuerySet
from django.test import TestCase

from project.filters import PlantProfileFilter
from project.models import NonNativeSpecies, PlantProfile, StratificationDuration


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

    def test_filter_no_stratification_required(self):
        no_strat = PlantProfile.objects.create(latin_name="No Strat Plant")
        zero_day = StratificationDuration.objects.create(stratification_duration=0)
        zero_day_plant = PlantProfile.objects.create(
            latin_name="Zero Day Strat", stratification_duration=zero_day
        )
        ninety_day = StratificationDuration.objects.create(stratification_duration=90)
        requires_strat = PlantProfile.objects.create(
            latin_name="Needs Strat", stratification_duration=ninety_day
        )
        double_dormant = PlantProfile.objects.create(
            latin_name="Double Dormant",
            stratification_duration=zero_day,
            double_dormancy=True,
        )

        filtered = self.filter.filter_no_stratification_required(
            self.queryset, "no_stratification_required", "No Stratification Required"
        )

        self.assertIn(no_strat, filtered)
        self.assertIn(zero_day_plant, filtered)
        self.assertNotIn(requires_strat, filtered)
        self.assertNotIn(double_dormant, filtered)

    def test_filter_non_native_name_matches_non_native_alternatives(self):
        native_alternative = PlantProfile.objects.create(latin_name="Asclepias syriaca")
        non_native = NonNativeSpecies.objects.create(
            latin_name="Buddleja davidii", english_name="Butterfly Bush"
        )
        native_alternative.substitute_for_non_native.add(non_native)

        filtered = self.filter.filter_non_native_name(
            self.queryset, "non_native_name", "butterfly bush"
        )

        self.assertIn(native_alternative, filtered)

    def test_filter_normalized_plant_name_does_not_match_non_native_alternatives(self):
        native_alternative = PlantProfile.objects.create(latin_name="Asclepias syriaca")
        non_native = NonNativeSpecies.objects.create(
            latin_name="Buddleja davidii", english_name="Butterfly Bush"
        )
        native_alternative.substitute_for_non_native.add(non_native)

        filtered = self.filter.filter_normalized_plant_name(
            self.queryset, "any_plant_name", "butterfly bush"
        )

        self.assertNotIn(native_alternative, filtered)
