# Import native substitutions for non-native species
# Imports the data from an Excel or CSV file with the following columns:
# first column: native species with latin name.  Header: latin_name
#
# subsequent columns: English common name of non-native followed by latin name between parentheses
# Header format: common name (latin name)
# Example:
# latin_name,Red Maple (Acer rubrum),Sugar Maple (Acer saccharum)
# Quercus rubra,Acer rubrum,Acer saccharum

# the intersection of the native species and non-native species is either yes or no to indicate if the native species is a substitute for the non-native species

# All native species must already exist in the PlantProfile model of the database.
# Non native species will be created if they do not already exist in the NonNativeSpecies model.
# if an Excel file is provided, it will be converted to CSV for processing.

import csv

import pandas as pd
from django.core.management.base import BaseCommand

from project.models import NonNativeSpecies, PlantProfile


class Command(BaseCommand):
    help = "Import non-native species substitutions from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="The path to the CSV file to import"
        )

    def handle(self, *args, **kwargs):

        file_path = kwargs["csv_file"]

        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            file_path = file_path.replace(".xlsx", ".csv")
            df.to_csv(file_path, index=False)

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)

            # Parse non-native species from headers
            non_native_species = []
            for header in headers[1:]:
                english_name, latin_name = header.rsplit("(", 1)
                latin_name = latin_name.rstrip(")")
                english_name = english_name.strip()
                non_native, created = NonNativeSpecies.objects.get_or_create(
                    latin_name=latin_name,
                    english_name=english_name,
                )
                non_native_species.append(non_native)

            # Process each row for native species and their substitutions
            for row in reader:
                native_latin_name = row[0]
                try:
                    native_species = PlantProfile.objects.get(
                        latin_name=native_latin_name
                    )
                except PlantProfile.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Native species not found: {native_latin_name}"
                        )
                    )
                    continue

                for i, cell in enumerate(row[1:]):
                    if cell.strip().lower() in ["yes", "y", "1", "true"]:
                        non_native = non_native_species[i]
                        native_species.substitute_for_non_native.add(non_native)

                native_species.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Processed substitutions for: {native_latin_name}"
                    )
                )


# End of importnonnativessubstitutions.py
