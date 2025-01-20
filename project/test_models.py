from django.core.exceptions import ValidationError
from django.test import TestCase

from project.models import PlantProfile


class PlantProfileHeightValidationTest(TestCase):
    """Test suite for PlantProfile height validation functionality.

    This TestCase class verifies the height validation logic in the PlantProfile model,
    specifically testing the compare_heights() method under various scenarios.

    Test cases include:
    - Valid height comparisons (min_height < max_height)
    - Equal heights (min_height = max_height)
    - Invalid height comparisons (min_height > max_height)
    - Null height values

    Attributes:
        plant (PlantProfile): Test PlantProfile instance initialized with a dummy latin name
    """

    def setUp(self):
        self.plant = PlantProfile(latin_name="Test Plant")

    def test_compare_heights_valid(self):
        """
        Test case to verify the compare_heights method with valid height values.

        Tests that when min_height (10) is less than max_height (20),
        the compare_heights() method executes without raising a ValidationError.

        Attributes:
            plant: Plant model instance used for testing

        Returns:
            None

        Raises:
            AssertionError: If ValidationError is raised unexpectedly
        """
        self.plant.min_height = 10
        self.plant.max_height = 20
        try:
            self.plant.compare_heights()
        except ValidationError:
            self.fail("compare_heights() raised ValidationError unexpectedly")

    def test_compare_heights_equal(self):
        """
        Test that compare_heights method validates successfully when min_height equals max_height.

        Tests that when min_height and max_height are set to the same value (10),
        the compare_heights() validation method executes without raising a ValidationError.
        This verifies that equal heights are considered valid.

        Raises:
            AssertionError: If compare_heights() raises a ValidationError when it should not
        """
        self.plant.min_height = 10
        self.plant.max_height = 10
        try:
            self.plant.compare_heights()
        except ValidationError:
            self.fail("compare_heights() raised ValidationError unexpectedly")

    def test_compare_heights_invalid(self):
        """
        Test that the compare_heights method raises a ValidationError when minimum height is greater than maximum height.

        Validates that:
        - A ValidationError is raised when min_height (20) is greater than max_height (10)
        - The error message contains "must be smaller than maximum height"
        """
        self.plant.min_height = 20
        self.plant.max_height = 10
        with self.assertRaises(ValidationError) as context:
            self.plant.compare_heights()
        self.assertTrue("must be smaller than maximum height" in str(context.exception))

    def test_compare_heights_null_values(self):
        """
        Tests the compare_heights method when both min_height and max_height are None.

        This test ensures that the compare_heights() method handles null values
        gracefully without raising a ValidationError. The test sets both min_height
        and max_height to None before calling compare_heights().

        Expected behavior:
            - Method should not raise a ValidationError when both height values are None
        """
        self.plant.min_height = None
        self.plant.max_height = None
        try:
            self.plant.compare_heights()
        except ValidationError:
            self.fail("compare_heights() raised ValidationError unexpectedly")


class PlantProfileSearchTest(TestCase):
    """Test suite for PlantProfile search functionality.

    This TestCase class verifies the search_plant_name functionality in the PlantProfile model,
    testing searches across latin_name, english_name, and french_name fields.
    """

    def setUp(self):
        """Set up test data with sample plant profiles."""
        self.plant1 = PlantProfile.objects.create(
            latin_name="Acer rubrum", english_name="Red Maple", french_name="Érable rouge"
        )
        self.plant2 = PlantProfile.objects.create(
            latin_name="Quercus alba", english_name="White Oak", french_name="Chêne blanc"
        )
        self.plant3 = PlantProfile.objects.create(
            latin_name="Acer saccharum", english_name="Sugar Maple", french_name="Érable à sucre"
        )

    def test_search_by_latin_name(self):
        """Test searching plants by Latin name."""
        results = PlantProfile.search_plant.plant_name("Acer")
        self.assertEqual(results.count(), 2)
        self.assertIn(self.plant1, results)
        self.assertIn(self.plant3, results)

    def test_search_by_english_name(self):
        """Test searching plants by English name."""
        results = PlantProfile.search_plant.plant_name("Maple")
        self.assertEqual(results.count(), 2)
        self.assertIn(self.plant1, results)
        self.assertIn(self.plant3, results)

    def test_search_by_french_name(self):
        """Test searching plants by French name."""
        results = PlantProfile.search_plant.plant_name("Érable")
        self.assertEqual(results.count(), 2)
        self.assertIn(self.plant1, results)
        self.assertIn(self.plant3, results)

    def test_case_insensitive_search(self):
        """Test that search is case insensitive."""
        results = PlantProfile.search_plant.plant_name("maple")
        self.assertEqual(results.count(), 2)
        self.assertIn(self.plant1, results)
        self.assertIn(self.plant3, results)

    def test_partial_match_search(self):
        """Test searching with partial text matches."""
        results = PlantProfile.search_plant.plant_name("blanc")
        self.assertEqual(results.count(), 1)
        self.assertIn(self.plant2, results)

    def test_no_results_search(self):
        """Test searching with text that should return no results."""
        results = PlantProfile.search_plant.plant_name("Pinaceae")
        self.assertEqual(results.count(), 0)
