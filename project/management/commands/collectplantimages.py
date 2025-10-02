# This command collects plant images from a specified directory and associates them with the correct plant profiles in the database.
# by default, it looks for images in 'media/plant_images_to_process' and moves them to 'media/plants/<plant_id>/'
# It assumes that the image filenames contain the plant's latin name followed by an underscore and the author name.
# Example: 'Rosa canina_Mario St-Gelais.jpg' would be associated with the plant having latin name 'Rosa canina' and author 'Mario St-Gelais'.
# If multiple images are found for the same plant, they will be numbered sequentially.
# Usage: python manage.py collectplantimages --source_dir=path/to/source --dest_dir=path/to/destination
# Default directories can be overridden with command line arguments.
# morphology_aspect field of PlantImage is set to 'Plant' by default.
# Existing images for a plant are not deleted or overwritten; new images are added alongside them.
# For each image found in the source directory, a PlantImage instance is created and linked to the corresponding Plant.
# If no matching plant is found for an image, a warning is printed and the image is skipped.
# The command provides feedback on the number of images processed and any issues encountered.
# Ensure that the MEDIA_ROOT setting in Django is correctly configured to point to the media directory.
# by providing the --force argument, existing PlantImage entries will be deleted before processing new images.  The corresponding image files will also be deleted. This is useful for reprocessing all images from scratch.
import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from project import utils
from project.management.commands.utils import (
    get_morphology_aspect,
    get_plant_by_latin_name,
)
from project.models import PlantImage, PlantProfile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Collect plant images from a specified directory and associate them with plant profiles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source_dir",
            type=str,
            default="plant_images_to_process",
            help="Directory to scan for plant images.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force the processing of images even if they don't match the expected pattern.",
        )

    def handle(self, *args, **options):
        source_dir: Path = Path(options["source_dir"])
        force = options["force"]

        if not source_dir.exists() or not source_dir.is_dir():
            self.stderr.write(
                f"Source directory '{source_dir}' does not exist or is not a directory."
            )
            return

        if force:
            self.stdout.write(
                "Force mode enabled. Data from Plant Images will be deleted first."
            )
            # Delete existing PlantImage entries to avoid duplicates
            PlantImage.objects.all().delete()

        image_files: list[Path] = list(source_dir.glob("*.*"))
        if not image_files:
            self.stdout.write(f"No images found in '{source_dir}'.")
            return

        processed_count = 0
        skipped_count = 0
        latin_names_processed = set()
        latin_names_duplicates = set()
        for source_image_path in image_files:
            match = re.match(
                r"^(?P<latin_name>.+?)_(?P<author>.+?)\.(jpg|jpeg|png|gif)$",
                source_image_path.name,
                re.IGNORECASE,
            )
            if not match:
                self.stderr.write(
                    f"Filename '{source_image_path.name}' does not match the expected pattern. Skipping."
                )
                skipped_count += 1
                continue

            latin_name = (
                match.group("latin_name").replace("_", " ").strip().capitalize()
            )
            if latin_name in latin_names_processed:
                self.stderr.write(
                    f"Latin name '{latin_name}' has already been processed. Skipping duplicate."
                )
                skipped_count += 1
                latin_names_duplicates.add(latin_name)
                continue
            latin_names_processed.add(latin_name)
            author = match.group("author").replace("_", " ").strip()

            plant: PlantProfile = get_plant_by_latin_name(latin_name)
            if not plant:
                self.stderr.write(
                    f"No plant found for '{latin_name}' by '{author}'. Skipping '{source_image_path.name}'."
                )
                skipped_count += 1
                continue

            # To be implemented when number field is added to PlantImage.
            # This will be used to ensure unique numbering of images when there are images in one morphology aspect.
            # max_number = existing_images.aggregate(Max("number"))["number__max"] or 0
            # new_number = max_number + 1
            new_number = 1

            slugified_filename = f"{slugify(plant.latin_name)}_{new_number}{source_image_path.suffix.lower()}"
            with source_image_path.open("rb") as img_file:
                # Define the upload path for the image
                upload_path = f"{plant.pk}/{slugified_filename}"
                plant_image: PlantImage = PlantImage(
                    plant_profile=plant,
                    image=File(
                        img_file,
                        name=upload_path,
                    ),
                    morphology_aspect=get_morphology_aspect("Plant"),
                    # number=new_number,
                    photo_author=author,
                    photo_date=timezone.now(),
                )
                plant_image_path = (
                    Path(settings.MEDIA_ROOT) / f"project/images/plants/{plant.pk}/"
                )
                # delete all files min plant image path and do not create the folder if it does not exist
                if plant_image_path.is_dir():
                    for existing_file in plant_image_path.glob("*.*"):
                        existing_file.unlink()

                plant_image.save()
            processed_count += 1
        self.stdout.write(
            f"Processing complete. {processed_count} images processed, {skipped_count} images skipped."
        )
        plants_without_images = utils.get_plants_without_images()
        if plants_without_images.exists():
            self.stdout.write(
                f"Plants without images: {plants_without_images.count()}. Consider adding images for them."
            )
            for plant in plants_without_images:
                self.stdout.write(f"- {plant.latin_name} (ID: {plant.pk})")
        if latin_names_duplicates:
            self.stdout.write(
                f"Duplicate latin names encountered: {', '.join(latin_names_duplicates)}"
            )
