# Image GPS Coordinates Command
# This command prints GPS coordinates from image metadata if available.
from django.core.management.base import BaseCommand
from exif import Image


class Command(BaseCommand):
    help = "Extract GPS coordinates from images"

    def add_arguments(self, parser):
        parser.add_argument("image_path", type=str, help="Path to the image file")
        # optional argument for searching directory recursively
        parser.add_argument(
            "--recursive", action="store_true", help="Search directory recursively"
        )

    def handle(self, *args, **kwargs):
        import glob
        import os

        image_path = kwargs["image_path"]
        recursive = kwargs["recursive"]

        if os.path.isdir(image_path):
            pattern = "**/*" if recursive else "*"
            image_files = glob.glob(
                os.path.join(image_path, pattern), recursive=recursive
            )
            image_files = [f for f in image_files if os.path.isfile(f)]
        else:
            image_files = [image_path]

        for img_file in image_files:
            try:
                with open(img_file, "rb") as img_f:
                    img = Image(img_f)
                    if (
                        img.has_exif
                        and hasattr(img, "gps_latitude")
                        and hasattr(img, "gps_longitude")
                    ):
                        lat = img.gps_latitude
                        lon = img.gps_longitude
                        lat_ref = img.gps_latitude_ref
                        lon_ref = img.gps_longitude_ref

                        lat_decimal = (
                            lat[0] + lat[1] / 60 + lat[2] / 3600
                            if lat_ref == "N"
                            else -(lat[0] + lat[1] / 60 + lat[2] / 3600)
                        )
                        lon_decimal = (
                            lon[0] + lon[1] / 60 + lon[2] / 3600
                            if lon_ref == "E"
                            else -(lon[0] + lon[1] / 60 + lon[2] / 3600)
                        )

                        self.stdout.write(
                            f"{img_file}: Latitude: {lat_decimal}, Longitude: {lon_decimal}"
                        )
                    # else:
                    # self.stdout.write(f"{img_file}: No GPS data found.")
            except Exception as e:
                self.stderr.write(f"Error processing {img_file}: {e}")
