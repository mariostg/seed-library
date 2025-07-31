# this command fetches the latest iNaturalist taxonomy and updates the local database
import pandas as pd
from django.core.management.base import BaseCommand

from project import models


class Command(BaseCommand):
    help = "Fetches the latest iNaturalist taxonomy and updates the local database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update even if the taxonomy is already up to date",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Output detailed information during the update process",
        )
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the file containing the iNaturalist taxonomy",
        )

    def read_csv_file(self, file_path):
        """Read a CSV file and return its contents as a DataFrame."""
        try:
            df = pd.read_csv(file_path)  # Read only the first 10 rows for debugging
            # retain only columns taxonID and scientificName
            df = df[df["kingdom"] == "Plantae"]  # Filter for kingdom Plants
            df = df[["taxonID", "scientificName"]]
            # Extract the last part of the taxonID after splitting by "/"
            df["taxonID"] = df["taxonID"].astype(str).str.split("/").str[-1]
            # filter for kingdom Plants
            return df
        except Exception as e:
            self.stderr.write(f"Error reading file {file_path}: {e}")
            return None

    def update_plant_profile_inaturalist_taxon(self, df):
        """Update the PlantProfile model with iNaturalist taxonomy data."""
        if df is None or df.empty:
            self.stderr.write("No data to update in PlantProfile.")
            return

        plants = models.PlantProfile.objects.all()
        counter = 0
        # for each plant, find the scientific_name  in the DataFrame and update the inaturalist_taxon field
        for plant in plants:
            counter += 1
            scientific_name = plant.latin_name
            matching_row = df[df["scientificName"] == scientific_name]
            if not matching_row.empty:
                taxon_id = matching_row["taxonID"].values[0]
                plant.inaturalist_taxon = taxon_id
                if self.verbose:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updating {counter}/{len(plants)}: {scientific_name} with taxon ID {taxon_id}"
                        )
                    )
                plant.save()
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"No matching taxon ID found for {scientific_name}"
                    )
                )
                candidates_rows = df[
                    df["scientificName"].str.contains(scientific_name, case=False)
                ]
                if not candidates_rows.empty:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Candidates found for {scientific_name}: {candidates_rows['scientificName'].values}"
                        )
                    )

    def handle(self, *args, **options):
        self.verbose = options["verbose"]
        file_path = options["file_path"]

        if self.verbose:
            self.stdout.write("Starting iNaturalist taxonomy update...")

        # Here you would implement the logic to fetch and update the taxonomy
        # For example, you might read from the file_path and update the database

        if self.verbose:
            self.stdout.write("iNaturalist taxonomy update completed successfully.")

        df = self.read_csv_file(file_path)
        self.update_plant_profile_inaturalist_taxon(df)
        self.stdout.write(
            self.style.SUCCESS("iNaturalist taxonomy update completed successfully.")
        )
