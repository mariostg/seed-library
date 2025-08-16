# from the specified CSV file, import the obsolete names into the database
# The CSV file should have two columns: "latin_name" and "obsolete_name"
# Each row in the CSV corresponds to an obsolete name for a specific plant.
# latin_name must exist in the PlantProfile table.
# Verifies that the latin name exists in the PlantProfile table before proceeding with the import.
# If there are latin names that don't exist, print the missing names and confirm with the user to confirm execution.
# Before importing, print the numbers of records to be imported and the number of existing records.
# the content of table ObsoleteNames will be deleted before importing new data.
import csv

from django.core.management.base import BaseCommand

from project import models


class Command(BaseCommand):
    help = "Import obsolete names from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        not_found = []
        to_import: list[tuple[str, str]] = []

        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                latin_name = row["latin_name"]
                obsolete_name = row["obsolete_name"]

                if not models.PlantProfile.all_objects.filter(  # active and non active plants
                    latin_name=latin_name
                ).exists():
                    not_found.append(latin_name)
                else:
                    to_import.append((latin_name, obsolete_name))

        if not_found:
            self.stdout.write(
                self.style.WARNING("The following Latin names were not found:")
            )
            for name in not_found:
                self.stdout.write(f" - {name}")
            self.stdout.write(
                self.style.WARNING("Do you want to continue anyway? (y/n)")
            )
            confirm = input().strip().lower()
            if confirm != "y":
                self.stdout.write(self.style.ERROR("Import cancelled."))
                return

        self.stdout.write(
            self.style.SUCCESS(f"Found {len(to_import)} records to import.")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Existing records in ObsoleteNames: {models.ObsoleteNames.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                "This will delete all existing records in ObsoleteNames."
            )
        )
        self.stdout.write(self.style.WARNING("Do you want to continue? (y/n)"))
        confirm = input().strip().lower()
        if confirm != "y":
            self.stdout.write(self.style.ERROR("Import cancelled."))
            return

        # Delete existing records in ObsoleteNames
        models.ObsoleteNames.objects.all().delete()

        # Import new records
        for latin_name, obsolete_name in to_import:
            plant = models.PlantProfile.all_objects.get(latin_name=latin_name)
            models.ObsoleteNames.objects.create(
                latin_name=plant, obsolete_name=obsolete_name
            )
        self.stdout.write(self.style.SUCCESS("Import completed successfully."))
