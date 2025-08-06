from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from project import models


class Command(BaseCommand):
    help = "Set the image profile for each plant profile based on the latin name"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to set image profiles..."))
        plants = models.PlantProfile.objects.all()
        if not plants.exists():
            self.stdout.write(
                self.style.ERROR("No plant profiles found to update image profile.")
            )
            exit(1)

        for plant in plants:
            self.set_image_profile(plant)
        self.stdout.write(self.style.SUCCESS("Image profiles updated successfully."))

    def set_image_profile(self, plant_profile: models.PlantProfile):
        plant_latin_name = plant_profile.latin_name
        if not plant_latin_name:
            return

        # Define the directory to search in
        image_dir = Path(settings.BASE_DIR) / Path("static/images/plants/profile")

        # Check if directory exists
        if not image_dir.exists():
            self.stdout.write(
                self.style.WARNING(f"Image directory {image_dir} does not exist")
            )
            return

        # Check for any files that start with the plant's latin name
        matching_files = list(image_dir.glob(f"{plant_latin_name}*"))

        # Update has_image_profile based on whether matching files were found
        has_image = plant_profile.has_image_profile
        plant_profile.has_image_profile = len(matching_files) > 0
        plant_profile.save()
        if has_image != plant_profile.has_image_profile:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated has_image_profile for {plant_latin_name} to {plant_profile.has_image_profile}"
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"No change in image profile for {plant_latin_name}, remains {plant_profile.has_image_profile}"
                )
            )

        if plant_profile.has_image_profile:
            self.stdout.write(
                self.style.SUCCESS(f"Found profile image for {plant_latin_name}")
            )
