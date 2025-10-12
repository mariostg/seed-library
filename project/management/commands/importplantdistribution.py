from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from project.models import PlantProfile

# This script imports plant distribution data into the PlantProfile model table from a CSV file.
# The CSV header should contain the following columns:
# - latin_name: The common name of the plant
# - AB: Distribution status in Alberta (N, E, I, or "")
# - BC: Distribution status in British Columbia (N, E, I, or "")
# - MB: Distribution status in Manitoba (N, E, I, or "")
# - NB: Distribution status in New Brunswick (N, E, I, or "")
# - NL: Distribution status in Newfoundland and Labrador (N, E, I, or "")
# - NS: Distribution status in Nova Scotia (N, E, I, or "")
# - NT: Distribution status in Northwest Territories (N, E, I, or "")
# - NU: Distribution status in Nunavut (N, E, I, or "")
# - ON: Distribution status in Ontario (N, E, I, or "")
# - PE: Distribution status in Prince Edward Island (N, E, I, or "")
# - QC: Distribution status in Quebec (N, E, I, or "")
# - SK: Distribution status in Saskatchewan (N, E, I, or "")
# - YT: Distribution status in Yukon (N, E, I, or "")
# where N = Native, E = Extirpated, I = Introduced, "" = Anything else


class Command(BaseCommand):
    help = "Import plant distribution data from a CSV file into the PlantProfile model."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=Path,
            help="The path to the CSV file containing plant distribution data.",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        try:
            df = pd.read_csv(file_path)
            required_columns = [
                "latin_name",
                "AB",
                "BC",
                "MB",
                "NB",
                "NL",
                "NS",
                "NT",
                "NU",
                "ON",
                "PE",
                "QC",
                "SK",
                "YT",
            ]
            # replace any nan values with "-"
            df.fillna("-", inplace=True)
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")

            with transaction.atomic():
                for _, row in df.iterrows():
                    latin_name = row["latin_name"].strip().capitalize()
                    try:
                        profile: PlantProfile = PlantProfile.objects.get(
                            latin_name=latin_name
                        )
                    except PlantProfile.DoesNotExist:
                        self.stderr.write(
                            self.style.WARNING(
                                f"PlantProfile not found for {latin_name}"
                            )
                        )
                        continue
                    profile.is_native_to_AB = True if row["AB"] == "N" else False
                    profile.is_native_to_BC = True if row["BC"] == "N" else False
                    profile.is_native_to_MB = True if row["MB"] == "N" else False
                    profile.is_native_to_NB = True if row["NB"] == "N" else False
                    profile.is_native_to_NL = True if row["NL"] == "N" else False
                    profile.is_native_to_NS = True if row["NS"] == "N" else False
                    profile.is_native_to_NT = True if row["NT"] == "N" else False
                    profile.is_native_to_NU = True if row["NU"] == "N" else False
                    profile.is_native_to_ON = True if row["ON"] == "N" else False
                    profile.is_native_to_PE = True if row["PE"] == "N" else False
                    profile.is_native_to_QC = True if row["QC"] == "N" else False
                    profile.is_native_to_SK = True if row["SK"] == "N" else False
                    profile.is_native_to_YT = True if row["YT"] == "N" else False
                    profile.save()
                    # print all plant profile is_native_to_* values
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated PlantProfile for {latin_name}")
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_AB: {profile.is_native_to_AB}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_BC: {profile.is_native_to_BC}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_MB: {profile.is_native_to_MB}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_NB: {profile.is_native_to_NB}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_NL: {profile.is_native_to_NL}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_NS: {profile.is_native_to_NS}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_NT: {profile.is_native_to_NT}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_NU: {profile.is_native_to_NU}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_ON: {profile.is_native_to_ON}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_PE: {profile.is_native_to_PE}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_QC: {profile.is_native_to_QC}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_SK: {profile.is_native_to_SK}"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  is_native_to_YT: {profile.is_native_to_YT}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    "Plant distribution data import completed successfully."
                )
            )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error importing plant distribution data: {e}")
            )
            raise e
