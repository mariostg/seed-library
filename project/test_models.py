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
