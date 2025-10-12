# Image GPS Coordinates Command
# This command prints GPS coordinates from image metadata if available.
import glob
import os

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
        # optional command to flush gps coordinates from images in a directory
        # this can be called separately from the command line
        # e.g. python manage.py imagegpscoord --flush /path/to/images
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Remove all GPS coordinates from images",
        )

    # a function to remove all gps coordinates from images in a directory
    def flush_gps_coordinates(self, image_path):
        self.stdout.write("Flushing GPS coordinates...")

        if os.path.isdir(image_path):
            pattern = "**/*"
            image_files = glob.glob(os.path.join(image_path, pattern), recursive=True)
            image_files = [f for f in image_files if os.path.isfile(f)]
        else:
            image_files = [image_path]

        for img_file in image_files:
            has_gps = False
            try:
                with open(img_file, "rb") as img_f:
                    img = Image(img_f)
                    if img.has_exif:
                        if hasattr(img, "gps_latitude"):
                            has_gps = True
                            self.stdout.write(
                                f"Flushing GPS latitude {img.gps_latitude} from {img_file}"
                            )
                            del img.gps_latitude
                            self.stdout.write(
                                f"still has gps_latitude? {hasattr(img, 'gps_latitude')}"
                            )
                        if hasattr(img, "gps_longitude"):
                            has_gps = True
                            self.stdout.write(
                                f"Flushing GPS longitude {img.gps_longitude} from {img_file}"
                            )
                            del img.gps_longitude
                            self.stdout.write(
                                f"still has gps_longitude? {hasattr(img, 'gps_longitude')}"
                            )
                        if hasattr(img, "gps_latitude_ref"):
                            has_gps = True
                            self.stdout.write(
                                f"Flushing GPS latitude reference {img.gps_latitude_ref} from {img_file}"
                            )
                            del img.gps_latitude_ref
                        if hasattr(img, "gps_longitude_ref"):
                            has_gps = True
                            self.stdout.write(
                                f"Flushing GPS longitude reference {img.gps_longitude_ref} from {img_file}"
                            )
                            del img.gps_longitude_ref

                        if has_gps:
                            with open(img_file, "wb") as new_img_f:
                                self.stdout.write(f"Writing changes to {img_file}")
                                new_img_f.write(img.get_file())
            except Exception as e:
                self.stderr.write(f"Error processing {img_file}: {e}")

    def print_gps_coordinates(self, image_path, recursive):
        self.stdout.write("Printing GPS coordinates...")

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

    def handle(self, *args, **kwargs):

        image_path = kwargs["image_path"]
        recursive = kwargs["recursive"]

        if kwargs["flush"]:
            self.flush_gps_coordinates(image_path)
        else:
            self.print_gps_coordinates(image_path, recursive)
