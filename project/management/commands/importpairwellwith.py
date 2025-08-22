import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from main.settings import DEBUG
from project import models


class Command(BaseCommand):
    """
    Django management command to import plant companion relationships from a CSV file.

    This command reads a CSV file containing information about plants that pair well together
    (companion plants) and creates PlantCompanion model instances to represent these relationships
    in the database.

    The CSV file should have the following columns:
    - latin_name: Latin name of the main plant
    - plant1, plant2, plant3, plant4, plant5: Latin names of companion plants

    For each valid row in the CSV, the command:
    1. Finds the main plant in the database using its latin_name
    2. Finds each companion plant in the database
    3. Creates a PlantCompanion relationship between the main plant and each companion plant

    The command will exit if the main plant is not found, and will skip rows where companion
    plants cannot be found in the database.

    Example usage:
        python manage.py importpairwellwith path/to/companion_plants.csv
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=Path,
            help="Path to the file containing the iNaturalist taxonomy",
        )
        # add argument --delete that will delete all existing PlantCompanion relationships
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all existing PlantCompanion relationships before importing",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            models.PlantCompanion.objects.all().delete()
            if DEBUG:
                self.stdout.write("Deleted all existing PlantCompanion relationships.")

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

        # Extract companion plants from the row and store them in a list
        companion_plants = []
        for i in range(1, 6):
            plant_key = f"plant{i}"
            plant_name = row.get(plant_key, "").strip().capitalize()
            if plant_name:
                try:
                    companion_plant_obj = models.PlantProfile.objects.get(
                        latin_name=plant_name
                    )
                    companion_plants.append(companion_plant_obj)
                except models.PlantProfile.DoesNotExist:
                    self.stderr.write(
                        f"Companion plant not found: {plant_name},skipping\n\n"
                    )
                    return
        # Create the PlantCompanion instance for each companion plant
        for companion_plant in companion_plants:
            pair_well_with = models.PlantCompanion(
                plant_profile=plant_obj,
                companion=companion_plant,
            )
            pair_well_with.save()
            self.stdout.write(
                f"\tCreated PlantCompanion relationship for {latin_name} with {companion_plant.latin_name}"
            )

        self.stdout.write(f"Finished processing row for plant: {latin_name}\n\n")
