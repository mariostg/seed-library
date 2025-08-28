# Import plant property data from CSV or Excel file
# Usage: python manage.py import_plant_property <file_path>
# If the file is an Excel file, it will be converted to CSV before importing.
# The file must contain 2 columns: the first column is the latin plant name, and the second column is the property value.
# The first row is the header and will be skipped. The first column of the first row must be "latin_name".
# The second column of the first row must be the property name.
# The property name will be used as the field name in the database.
# Before importing, the command will check if the latin name exists in the database Plant profile model.
# A list of not found latin names will be printed and the import will be aborted.
# Before importing, the command will check if the property exists in the database Plant profile model.
# If the property does not exist, import will be aborted.
# If the property is a foreign key, the command will check if the foreign key value exists in the database and create it if it does not exist.
# Property will not be updated if it is not different from the existing value.
# A summary of the import results will be printed.
import csv

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import models

from project.models import PlantProfile


class Command(BaseCommand):
    """
    Django management command to import plant property data from CSV or Excel files.

    This command allows users to import and update single property values for PlantProfile
    model instances. The input file must be either CSV or Excel format with two columns:
    1. 'latin_name' - The latin name of the plant to update
    2. The name of the property to update - This must be a valid field name in PlantProfile model

    Examples:
        # Import from CSV file
        python manage.py import_plant_property path/to/file.csv

        # Import from Excel file
        python manage.py import_plant_property path/to/file.xlsx

    Notes:
        - The command will convert Excel files to CSV automatically
        - Property values are converted appropriately:
            - "yes"/"y" to True
            - "no"/"n" to False
            - Numeric strings to float
            - Other values remain as strings
        - Only plants that need updating will be modified
        - Plants not found in the database will be reported
    """

    help = "Import plant property data from CSV or Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV or Excel file")

    def handle(self, *args, **options):
        self.file_path = options["file_path"]
        if self.file_path.endswith(".csv"):
            self.import_csv(self.file_path)
        elif self.file_path.endswith(".xls") or self.file_path.endswith(".xlsx"):
            csv_file_path = self.convert_excel_to_csv(self.file_path)
            self.import_csv(csv_file_path)
        else:
            self.stdout.write(
                self.style.ERROR(
                    "Unsupported file format. Please provide a CSV or Excel file."
                )
            )

    def convert_excel_to_csv(self, file_path):
        # Implement the conversion logic here
        df = pd.read_excel(file_path)
        csv_file_path = file_path.rsplit(".", 1)[0] + ".csv"
        df.to_csv(csv_file_path, index=False)
        return csv_file_path

    def convert_property_value_format(self, value):
        # handle yes and no values
        if value.lower() in ["yes", "y"]:
            return True
        elif value.lower() in ["no", "n"]:
            return False
        # handle numeric values
        try:
            return float(value)
        except ValueError:
            return value

    def import_csv(self, file_path):
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            if len(header) != 2 or header[0].lower() != "latin_name":
                self.stdout.write(
                    self.style.ERROR(
                        'Invalid CSV format. The first column must be "latin_name".'
                    )
                )
                return
            property_name = header[1]
            if not hasattr(PlantProfile, property_name):
                self.stdout.write(
                    self.style.ERROR(
                        f'Property "{property_name}" does not exist in PlantProfile.'
                    )
                )
                return
            not_found = []
            updated = 0
            skipped_count = 0
            for row in reader:
                latin_name = row[0].strip().capitalize()
                value = self.convert_property_value_format(row[1])
                try:
                    plant = PlantProfile.objects.get(latin_name=latin_name)
                except PlantProfile.DoesNotExist:
                    not_found.append(latin_name)
                    continue
                current_value = getattr(plant, property_name)
                if str(current_value) != str(value):
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updating {latin_name}: {property_name} from {current_value} to {value}"
                        )
                    )
                    # if property name is a foreign key, check if the value exists in the foreign key model and create the value
                    if isinstance(
                        getattr(PlantProfile, property_name).field, models.ForeignKey
                    ):
                        related_model = getattr(
                            PlantProfile, property_name
                        ).field.related_model
                        value, created = related_model.objects.get_or_create(
                            **{property_name: value}
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created new related {related_model.__name__} entry: {value}"
                                )
                            )
                    setattr(plant, property_name, value)
                    try:
                        plant.save()
                        updated += 1
                    except ValueError:
                        self.stdout.write(
                            self.style.ERROR(f"Error updating {latin_name}: {value}")
                        )
                else:
                    skipped_count += 1

            if not_found:
                self.stdout.write(
                    self.style.ERROR(f'Latin names not found: {", ".join(not_found)}')
                )
        self.stdout.write(self.style.SUCCESS(f"Updated: {updated}"))
        self.stdout.write(
            self.style.WARNING(f"Skipped (no change needed): {skipped_count}")
        )

        # Implement the import logic here
