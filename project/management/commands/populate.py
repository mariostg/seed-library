"""
Typical usage:
    python manage.py populate

Populate command uses the data available from the test-data folder.  This folder contains all the CSV files necessary to set up the system initially.

!!! warning
    It will overwrite all existing data in the system.

"""

from pathlib import Path

from django.core.management.base import BaseCommand

from main.settings import DEBUG
from project import models, uploadprocessor


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            action="store",
            help="Specify the path of the csv file.",
        )

    def handle(self, *args, filepath, **options):
        if DEBUG:
            self.filepath = Path(filepath)
            models.PlantProfile.objects.all().delete()
            models.SharingPriority.objects.all().delete()
            models.HarvestingIndicator.objects.all().delete()
            models.SeedHead.objects.all().delete()
            models.HarvestingMean.objects.all().delete()
            models.ViablityTest.objects.all().delete()
            models.SeedStorage.objects.all().delete()
            models.SowingDepth.objects.all().delete()
            models.PackagingMeasure.objects.all().delete()
            models.OneCultivar.objects.all().delete()
            models.Dormancy.objects.all().delete()
            models.SeedPreparation.objects.all().delete()
            models.SeedStorageLabelInfo.objects.all().delete()
            models.Lighting.objects.all().delete()
            models.SoilHumidity.objects.all().delete()
            self.set_sharing_priority()
            self.set_harvesting_indicator()
            self.set_seed_head()
            self.set_harvesting_mean()
            self.set_viability_test()
            self.set_seed_storage()
            self.set_sowing_depth()
            self.set_packaging_measure()
            self.set_one_cultivar()
            self.set_dormancy()
            self.set_seed_preparation()
            self.set_storage_label_info()
            self.set_lighting()
            self.set_soil_humidity()

            self.set_seed_library()
        else:
            raise ValueError("This capability is only available when DEBUG is True")

    def set_seed_library(self):
        filepath = self.filepath / "seed-library.csv"
        uploadprocessor.PlantProfileProcessor(filepath).main()

    def set_sharing_priority(self):
        filepath = self.filepath / "sharing-priority.csv"
        uploadprocessor.CsvProcessor(filepath, "sharing_priority", models.SharingPriority).main()

    def set_harvesting_indicator(self):
        filepath = self.filepath / "harvesting-indicator.csv"
        uploadprocessor.CsvProcessor(filepath, "harvesting_indicator", models.HarvestingIndicator).main()

    def set_seed_head(self):
        filepath = self.filepath / "seed-head.csv"
        uploadprocessor.CsvProcessor(filepath, "seed_head", models.SeedHead).main()

    def set_harvesting_mean(self):
        filepath = self.filepath / "harvesting-mean.csv"
        uploadprocessor.CsvProcessor(filepath, "harvesting_mean", models.HarvestingMean).main()

    def set_viability_test(self):
        filepath = self.filepath / "viability-test.csv"
        uploadprocessor.CsvProcessor(filepath, "viability_test", models.ViablityTest).main()

    def set_seed_storage(self):
        filepath = self.filepath / "seed-storage.csv"
        uploadprocessor.CsvProcessor(filepath, "seed_storage", models.SeedStorage).main()

    def set_sowing_depth(self):
        filepath = self.filepath / "sowing-depth.csv"
        uploadprocessor.CsvProcessor(filepath, "sowing_depth", models.SowingDepth).main()

    def set_packaging_measure(self):
        filepath = self.filepath / "packaging-measure.csv"
        uploadprocessor.CsvProcessor(filepath, "packaging_measure", models.PackagingMeasure).main()

    def set_one_cultivar(self):
        filepath = self.filepath / "one-cultivar.csv"
        uploadprocessor.CsvProcessor(filepath, "one_cultivar", models.OneCultivar).main()

    def set_dormancy(self):
        filepath = self.filepath / "dormancy.csv"
        uploadprocessor.CsvProcessor(filepath, "dormancy", models.Dormancy).main()

    def set_seed_preparation(self):
        filepath = self.filepath / "seed-preparation.csv"
        uploadprocessor.CsvProcessor(filepath, "seed_preparation", models.SeedPreparation).main()

    def set_storage_label_info(self):
        filepath = self.filepath / "seed-storage-label-info.csv"
        uploadprocessor.CsvProcessor(filepath, "seed_storage_label_info", models.SeedStorageLabelInfo).main()

    def set_lighting(self):
        filepath = self.filepath / "lighting.csv"
        uploadprocessor.CsvProcessor(filepath, "lighting", models.Lighting).main()

    def set_soil_humidity(self):
        filepath = self.filepath / "soil-humidity.csv"
        uploadprocessor.CsvProcessor(filepath, "soil_humidity", models.SoilHumidity).main()
