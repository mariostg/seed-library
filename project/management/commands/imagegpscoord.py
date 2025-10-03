# Image GPS Coordinates Command
# This command prints GPS coordinates from image metadata if available.
from django.core.management.base import BaseCommand
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


class Command(BaseCommand):
    help = "Extract GPS coordinates from images"

    def add_arguments(self, parser):
        parser.add_argument("image_path", type=str, help="Path to the image file")
        # optional argument for searching directory recursively
        parser.add_argument(
            "--recursive", action="store_true", help="Search directory recursively"
        )

    def handle(self, *args, **kwargs):
        image_path = kwargs["image_path"]
        recursive = kwargs["recursive"]
        if recursive:
            import os

            for root, _dirs, files in os.walk(image_path):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        full_path = os.path.join(root, file)
                        # self.stdout.write(f"Processing {full_path}")
                        self.extract_gps_coordinates(full_path)
        else:
            self.extract_gps_coordinates(image_path)

    def extract_gps_coordinates(self, image_path):
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if not exif_data:
                self.stdout.write(self.style.WARNING("No EXIF data found"))
                return

            gps_info = None
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "GPSInfo":
                    gps_info = value
                    break

            if not gps_info:
                # self.stdout.write(self.style.WARNING("No GPS information found"))
                return

            latitude = self.get_geotag(gps_info, GPSTAGS["GPSLatitude"])
            longitude = self.get_geotag(gps_info, GPSTAGS["GPSLongitude"])

            if latitude and longitude:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"GPS Coordinates: {latitude}, {longitude} in {image_path}"
                    )
                )
            else:
                self.stdout.write(self.style.WARNING("Incomplete GPS information"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def get_geotag(self, gps_info, tag):
        return gps_info.get(tag)
