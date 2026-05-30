from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from project.models import PlantProfile, StratificationDuration


class AnalyzePlantProfilesCommandTest(TestCase):
    def test_reports_double_dormancy_without_stratification(self):
        PlantProfile.objects.create(
            latin_name="Invalid Plant",
            double_dormancy=True,
            inaturalist_taxon="12345",
        )
        duration = StratificationDuration.objects.create(stratification_duration=90)
        PlantProfile.objects.create(
            latin_name="Valid Plant",
            double_dormancy=True,
            stratification_duration=duration,
            inaturalist_taxon="67890",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "double_dormancy_requires_stratification",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("double_dormancy_requires_stratification", output)
        self.assertIn("Invalid plant", output)
        self.assertNotIn("Valid plant", output)
        self.assertIn("1 issue(s) found", output)

    def test_fail_on_issues_raises_command_error(self):
        PlantProfile.objects.create(
            latin_name="Invalid Plant",
            double_dormancy=True,
            inaturalist_taxon="12345",
        )

        with self.assertRaisesMessage(CommandError, "1 issue(s) found"):
            call_command(
                "analyze_plant_profiles",
                "--check",
                "double_dormancy_requires_stratification",
                "--fail-on-issues",
            )

    def test_reports_missing_inaturalist_taxon(self):
        PlantProfile.objects.create(
            latin_name="Missing Taxon",
            inaturalist_taxon="",
        )
        PlantProfile.objects.create(
            latin_name="Has Taxon",
            inaturalist_taxon="12345",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "missing_inaturalist_taxon",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("missing_inaturalist_taxon", output)
        self.assertIn("Missing taxon", output)
        self.assertNotIn("Has taxon", output)
        self.assertIn("1 issue(s) found", output)

    def test_reports_missing_taxon(self):
        PlantProfile.objects.create(
            latin_name="Missing Vascan Taxon",
            taxon="",
            inaturalist_taxon="12345",
        )
        PlantProfile.objects.create(
            latin_name="Has Vascan Taxon",
            taxon="54321",
            inaturalist_taxon="67890",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "missing_taxon",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("missing_taxon", output)
        self.assertIn("Missing vascan taxon", output)
        self.assertNotIn("Has vascan taxon", output)
        self.assertIn("1 issue(s) found", output)
