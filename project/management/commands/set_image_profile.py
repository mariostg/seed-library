import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from project import models


class Command(BaseCommand):
    help = "Set the image profile for each plant profile based on the latin name"

    def add_arguments(self, parser):
        parser.add_argument(
            "directory",
            type=Path,
            help="The directory containing plant images to be processed.",
        )

    def handle(self, *args, **kwargs):
        self.unfound_latin_names = []
        directory = kwargs["directory"]
        if not directory.is_dir():
            self.stdout.write(self.style.ERROR("Invalid directory path."))
            exit(1)
        self.stdout.write(self.style.SUCCESS(f"Processing images in {directory}..."))
        image_paths = list(directory.glob("*.jpg"))
        image_paths += list(directory.glob("*.JPG"))
        self.set_all_has_image_false()
        for image_path in image_paths:
            self.process_image(image_path)
        if self.unfound_latin_names:
            self.stdout.write(
                self.style.WARNING(
                    "The following latin names were not found in the database:\n"
                    + "\n".join(self.unfound_latin_names)
                )
            )

    def set_all_has_image_false(self):
        # Set has_image_profile to False for all plant profiles
        models.PlantProfile.objects.all().update(has_image_profile=False)
        self.stdout.write(
            self.style.SUCCESS(
                "All plant profiles have been set to not have an image profile."
            )
        )

    def _split_image_name(self, image_path: Path):
        # image name is made of the latin name, followed by an underscore and the author name
        plant_latin_name, author = image_path.stem.split("_")
        plant_latin_name = plant_latin_name.strip()
        author = author.strip()
        return plant_latin_name, author

    def process_image(self, image_path: Path):
        plant_latin_name, author = self._split_image_name(image_path)
        try:
            plant_profile = models.PlantProfile.objects.get(latin_name=plant_latin_name)
            # if plant_profile exists, set has_image_profile to True and copy the image to the media directory
            plant_profile.has_image_profile = True
            plant_profile.save()
            # rename the image file to match the plant profile's latin name
            destination_dir = settings.BASE_DIR / "static/images/plants/profile"
            new_image_path = destination_dir / f"{plant_latin_name}-profile.jpg"
            # Create destination directory if it doesn't exist
            destination_dir.mkdir(parents=True, exist_ok=True)
            # Copy the image file to the destination
            shutil.copy2(image_path, new_image_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Image {image_path.name} processed and saved as {new_image_path.name}."
                )
            )
        except models.PlantProfile.DoesNotExist:
            self.unfound_latin_names.append(plant_latin_name)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred while processing {image_path.name}: {e}"
                )
            )
