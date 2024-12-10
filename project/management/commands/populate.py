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

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            action="store",
            help="Specify the path of the csv file.",
        )

    def handle(self, *args, filepath, **options):
        print("FILAPATH: ", filepath)
        if DEBUG:
            filepath = Path(filepath)
            models.SeedLibrary.objects.all().delete()
            self.set_seed_library(filepath)
        else:
            print("This capability is only available when DEBUG is True")

    def set_seed_library(self, filepath):
        uploadprocessor.SeedLibraryProcessor(filepath).main()
