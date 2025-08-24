import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from main.settings import DEBUG
from project import models


class Command(BaseCommand):
    """
    Django management command to import plant complementary relationships from a CSV file.

    This command reads a CSV file containing information about plants that pair well together
    (complementary plants) and creates PlantComplementary model instances to represent these relationships
    in the database.

    The CSV file should have the following columns:
    - latin_name: Latin name of the main plant
    - plant1, plant2, plant3, plant4, plant5: Latin names of complementary plants

    For each valid row in the CSV, the command:
    1. Finds the main plant in the database using its latin_name
    2. Finds each complementary plant in the database
    3. Creates a PlantComplementary relationship between the main plant and each complementary plant

    The command will exit if the main plant is not found, and will skip rows where complementaryplants cannot be found in the database.

    Example usage:
        python manage.py importpairwellwith path/to/complementary_plants.csv
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=Path,
            help="Path to the file containing the iNaturalist taxonomy",
        )
        # add argument --delete that will delete all existing PlantComplementary relationships
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all existing PlantComplementary relationships before importing",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            models.PlantComplementary.objects.all().delete()
            if DEBUG:
                self.stdout.write(
                    "Deleted all existing PlantComplementary relationships."
                )

        csv_file = options["file_path"]
        if not csv_file or not csv_file.exists():
            self.stderr.write("Invalid CSV file path.")
            return

        with csv_file.open("r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.process_row(row)

    def process_row(self, row):
        latin_name = (
            row.get("latin_name").strip().capitalize()
            if row.get("latin_name")
            else None
        )
        self.stdout.write(self.style.SUCCESS(f"Processing row for plant: {latin_name}"))
        if not latin_name:
            self.stderr.write("Missing required fields in row.")
            exit(1)

        if latin_name:
            plant_obj = models.PlantProfile.objects.get(latin_name=latin_name)
            if not plant_obj:
                self.stderr.write(f"Plant not found: {latin_name}")
                exit(1)

        # Extract complementary plants from the row and store them in a list
        complementary_plants = []
        for i in range(1, 6):
            plant_key = f"plant{i}"
            plant_name = row.get(plant_key, "").strip().capitalize()
            if plant_name:
                try:
                    complementary_plant_obj = models.PlantProfile.objects.get(
                        latin_name=plant_name
                    )
                    complementary_plants.append(complementary_plant_obj)
                except models.PlantProfile.DoesNotExist:
                    self.stderr.write(
                        f"Complementary plant not found: {plant_name},skipping\n\n"
                    )
                    return
        # Create the PlantComplementary instance for each complementary plant
        for complementary_plant in complementary_plants:
            pair_well_with = models.PlantComplementary(
                plant_profile=plant_obj,
                complement=complementary_plant,
            )
            pair_well_with.save()
            self.stdout.write(
                f"\tCreated PlantComplementary relationship for {latin_name} with {complementary_plant.latin_name}"
            )

        self.stdout.write(f"Finished processing row for plant: {latin_name}\n\n")
