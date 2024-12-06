"""
Typical usage:
    python manage.py populate

Populate command uses the data available from the test-data folder.  This folder contains all the CSV files necessary to set up the system initially.

!!! warning
    It will overwrite all existing data in the system.

"""

from django.core.management.base import BaseCommand
from main.settings import DEBUG
from pathlib import Path
from project import models
from project import uploadprocessor
import os


class Command(BaseCommand):
    PWD = os.getenv("PWD")
    source_tables = Path(PWD).resolve() / "data/csv"

    def handle(self, *args, **options):
        if DEBUG:
            models.SeedLibrary.objects.all().delete()
            self.set_seed_library()
        else:
            print("This capability is only available when DEBUG is True")

    def set_seed_library(self):
        uploadprocessor.SeedLibraryProcessor(self.source_tables / "seed-library.csv").main()
