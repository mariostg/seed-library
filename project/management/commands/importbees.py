import csv
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand

from project.models import BeeSpecies, PlantProfile


class Command(BaseCommand):
    """
    Django management command for importing bee data from a CSV or Excel file.

    This command allows users to import bee species information and their
    relationships with plant profiles from a CSV file or an Excel file (which will
    be converted to CSV). The command validates that all plant profiles referenced
    in the import file exist in the database before proceeding with the import.

    The import file should contain:
    - A 'latin_name' column for plant names
    - Additional columns with naming format containing bee latin name where the key
        is in the format "bee-{latin_name}" and the value is "yes" or "no"
        indicating whether the plant supports the bee

    Usage:
            python manage.py importbees <file_path>

    Arguments:
            bee_file_path: Path to the bee data file (.csv or .xlsx)

    Example:
            python manage.py importbees data/bees.xlsx

    The command will:
    1. Convert .xlsx files to .csv if needed
    2. Validate that all referenced plant profiles exist in the database
    3. Process each row to extract bee information and plant associations
    4. Create bee species records if they don't already exist
    5. Update plant profile associations with bees
    help = "Import bee data from a CSV file"""

    def add_arguments(self, parser):
        parser.add_argument("bee_file_path", type=str, help="Path to the bee files")
        # add argument to process a directory of files instead of a single file
        parser.add_argument(
            "--directory",
            action="store_true",
            help="Process all files in the specified directory",
        )

    def handle(self, *args, **options):
        path = options["bee_file_path"]
        is_directory = options["directory"]

        if is_directory:
            # Process all files in directory
            dir_path = Path(path)
            if not dir_path.is_dir():
                self.stderr.write(f"'{path}' is not a directory.")
                return

            # Process all xlsx and csv files in the directory
            for file_path in dir_path.glob("*.xlsx"):
                self.process_file(file_path)
        else:
            # Process single file
            self.process_file(Path(path))

    def process_file(self, file_path: Path):
        """Process a single bee file."""
        self.bee_xlsx_file_path = None
        self.bee_csv_file_path = None

        if file_path.suffix.lower() == ".xlsx":
            self.bee_xlsx_file_path = file_path
            self.bee_csv_file_path = file_path.with_suffix(".csv")
        elif file_path.suffix.lower() == ".csv":
            self.bee_csv_file_path = file_path
            self.bee_xlsx_file_path = None
        else:
            self.stderr.write(f"File '{file_path}' is not an xlsx or csv file.")
            return

        self.main()

    def validate_plants(self, reader):
        """
        Validate that all plant latin names in the CSV file exist in the database.

        This method iterates through each row in the provided CSV reader and checks
        if a plant with the given latin name exists in the database. If any plant
        does not exist, it raises a ValueError.

        Args:
            reader: A CSV DictReader object containing plant data with at least
                   a 'latin_name' column.

        Raises:
            ValueError: If a plant with the specified latin name does not exist
                       in the database.

        Returns:
            None: Outputs a success message if all plants are validated successfully.
        """
        for row in reader:
            latin_name = row["latin_name"].strip().capitalize()
            if not PlantProfile.objects.filter(latin_name=latin_name).exists():
                raise ValueError(
                    f"Plant with latin name '{latin_name}' does not exist in the database."
                )
        # reset the file pointer to the beginning of the file after reading
        self.stdout.write(self.style.SUCCESS("All plants validated successfully."))

    def import_bees(self):
        """
        Import bees from a CSV file and associate them with plant profiles.

        This method reads a CSV file containing bee information, processes each row to extract
        bee details, creates or retrieves bee objects, and updates the associated
        plant profiles with these bees.

        The CSV file is expected to have columns that can be processed by the _process_bee_row
        method to extract plant latin names and bee information.

        Note:
            This method relies on _process_bee_row, _get_or_create_bee, and
            _update_plant_profile helper methods to process the data.
        """
        with open(self.bee_csv_file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    (
                        latin_name,
                        bee_latin_name,
                        is_supported,
                    ) = self._process_bee_row(row)
                except ValueError as e:
                    self.stderr.write(str(e))
                    raise (e)
                bee = self._get_or_create_bee(bee_latin_name)
                plant_profile = PlantProfile.objects.get(latin_name=latin_name)
                self._update_plant_profile(plant_profile, bee, is_supported)

    # convert an xlsx file to a csv file
    def _convert_xlsx_to_csv(self):
        """
        Convert an xlsx file to a csv file.

        Returns:
            None: Writes the converted data to the specified csv file.
        """
        try:
            df = pd.read_excel(self.bee_xlsx_file_path)
        except FileNotFoundError:
            self.stderr.write(
                f"File '{self.bee_xlsx_file_path}' not found. Please provide a valid xlsx file."
            )
            return
        except Exception as e:
            self.stderr.write(
                f"Error reading the xlsx file: {e}. Please ensure the file is a valid Excel file."
            )
            return
        df.to_csv(self.bee_csv_file_path, index=False)
        self.stdout.write(
            #  Write a success message to stdout indicating the conversion indicating only the file names
            self.style.SUCCESS(
                f"\nFrom {self.bee_xlsx_file_path.parent}\nconverted\t{self.bee_xlsx_file_path.name}\nto\t\t{self.bee_csv_file_path.name}"
            )
        )

    def _process_bee_row(self, row: dict) -> tuple:
        """
        Process a row of bee data from a CSV file.

        Args:
            row (dict): A dictionary containing the bee data.
                The first key is expected to be 'latin_name' with the value being the latin name of the plant.
                The second key is expected to be a string containing latin name of the bee
                with the value being either "yes" or "no" indicating if the plant supports
                the bee.

        Returns:
            tuple: A tuple containing:
                - latin_name (str): The latin name of the plant
                - bee_latin_name (str): The latin name of the bee
                - is_supported (bool): True if the plant supports the bee, False otherwise

        Raises:
            ValueError: If the 'latin_name' key is missing from the row.
        """

        if "latin_name" not in row:
            raise ValueError("CSV row must contain a 'latin_name' key.")
        latin_name = (
            row["latin_name"].strip().capitalize()
        )  # the latin name of the plant
        # then second key of row is the english name and latin name of the bee separated by a hyphen
        bee_info = list(row.keys())[1]  # the second key of the row
        is_supported = row[bee_info].strip().lower() == "yes"
        _, bee_latin_name = bee_info.split("-")  # split the string latin name

        return latin_name, bee_latin_name, is_supported

    def _get_or_create_bee(self, bee_latin_name: str) -> BeeSpecies:
        """
        Get an existing bee species or create a new one if it doesn't exist.

        This method attempts to retrieve a bee species by its Latin name.
        If the species doesn't exist in the database, it creates a new entry with
        the provided Latin name.

        Args:
            bee_latin_name (str): The Latin name of the bee species

        Returns:
            BeeSpecies: The retrieved or newly created bee species object

        Side effects:
            - Writes success message to stdout when a new species is created
        """
        bee, created = BeeSpecies.objects.get_or_create(
            latin_name=bee_latin_name,
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created new bee species: {bee_latin_name}")
            )
        return bee

    def _update_plant_profile(
        self,
        plant_profile: PlantProfile,
        bee: BeeSpecies,
        is_supported: bool,
    ):
        """
        Update the plant profile with the bee species.

        This method adds the bee species to the plant profile's bees field
        if it is not already present. If the plant supports the bee, it adds it to
        the bees field; otherwise, it removes it.

        Args:
            plant_profile (PlantProfile): The plant profile to update
            bee (BeeSpecies): The bee species to add or remove
            is_supported (bool): True if the plant supports the bee, False otherwise

        Returns:
            None: Updates the plant profile in place
        """
        if is_supported:
            if bee not in plant_profile.bees.all():
                plant_profile.bees.add(bee)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added {bee.latin_name} to {plant_profile.latin_name} bees."
                    )
                )
        else:
            if bee in plant_profile.bees.all():
                plant_profile.bees.remove(bee)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Removed {bee.latin_name} from {plant_profile.latin_name} bees."
                    )
                )
        plant_profile.save()

    # Open the csv file and read the latin names of the plants and verifies that they exist in the database.
    def main(self):
        self._convert_xlsx_to_csv()
        try:
            with open(self.bee_csv_file_path) as f:
                reader = csv.DictReader(f)
                self.validate_plants(reader)
        except FileNotFoundError:
            self.stderr.write(f"File '{self.bee_csv_file_path}' not found.")
            return
        except ValueError as e:
            self.stderr.write(str(e))
            return
        self.import_bees()
