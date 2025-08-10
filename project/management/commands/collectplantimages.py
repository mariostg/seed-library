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
import logging
import re
import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

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
            "--dest_dir",
            type=str,
            default="plants",
            help="Directory to store processed plant images.",
        )

    def handle(self, *args, **options):
        source_dir: Path = Path(options["source_dir"])
        dest_dir: Path = Path(settings.MEDIA_ROOT) / options["dest_dir"]

        if not source_dir.exists() or not source_dir.is_dir():
            self.stderr.write(
                f"Source directory '{source_dir}' does not exist or is not a directory."
            )
            return

        dest_dir.mkdir(parents=True, exist_ok=True)

        image_files: list[Path] = list(source_dir.glob("*.*"))
        if not image_files:
            self.stdout.write(f"No images found in '{source_dir}'.")
            return

        processed_count = 0
        skipped_count = 0

        for image_path in image_files:
            match = re.match(
                r"^(?P<latin_name>.+?)_(?P<author>.+?)\.(jpg|jpeg|png|gif)$",
                image_path.name,
                re.IGNORECASE,
            )
            if not match:
                self.stderr.write(
                    f"Filename '{image_path.name}' does not match the expected pattern. Skipping."
                )
                skipped_count += 1
                continue

            latin_name = match.group("latin_name").replace("_", " ").strip()
            author = match.group("author").replace("_", " ").strip()

            plant: PlantProfile = get_plant_by_latin_name(latin_name)
            if not plant:
                self.stderr.write(
                    f"No plant found for '{latin_name}' by '{author}'. Skipping '{image_path.name}'."
                )
                skipped_count += 1
                continue
            plant_image_dir = dest_dir / str(plant.pk)
            plant_image_dir.mkdir(parents=True, exist_ok=True)

            # To be implemented when number field is added to PlantImage.
            # This will be used to ensure unique numbering of images when there are images in one morphology aspect.
            # max_number = existing_images.aggregate(Max("number"))["number__max"] or 0
            # new_number = max_number + 1
            new_number = 1

            new_filename = (
                f"{slugify(plant.latin_name)}_{new_number}{image_path.suffix.lower()}"
            )
            new_image_path = plant_image_dir / new_filename
            shutil.move(str(image_path), new_image_path)
            with new_image_path.open("rb") as img_file:
                plant_image = PlantImage(
                    plant_profile=plant,
                    image=File(img_file, name=new_filename),
                    morphology_aspect=get_morphology_aspect("Plant"),
                    # number=new_number,
                    photo_author=author,
                    photo_date=timezone.now(),
                )
                plant_image.save()
            processed_count += 1
            self.stdout.write(
                f"Processed image '{new_filename}' for plant '{plant.latin_name}'."
            )
        self.stdout.write(
            f"Processing complete. {processed_count} images processed, {skipped_count} images skipped."
        )
