import base64
from io import BytesIO
from pathlib import Path

import qrcode
from django.http import HttpRequest
from exif import Image
from PIL import Image as PILImage

from project.models import PlantImage, PlantProfile

MONTHS = {
    0: "",
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def all_plants(request):
    return PlantProfile.objects.all()


def single_plant(pk, request: HttpRequest):
    if request.user.is_authenticated:
        plant = PlantProfile.all_objects.get(pk=pk)
    else:
        try:
            plant = PlantProfile.objects.get(pk=pk)
        except PlantProfile.DoesNotExist:
            plant = None

    # plant.bloom_start = MONTHS.get(plant.bloom_start, "")
    # plant.bloom_end = MONTHS.get(plant.bloom_end, "")

    # plant.harvesting_start = MONTHS[plant.harvesting_start]
    return plant


def plant_primary_image(plant: PlantProfile):
    plant_image = PlantImage.objects.filter(
        plant_profile=plant, morphology_aspect=7
    ).first()
    return plant_image


def resize_image(image_path: str, max_width: int, max_height: int):
    with PILImage.open(image_path) as img:
        img.thumbnail((max_width, max_height))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        return buffered


def plant_light_range(plant: PlantProfile):
    if plant.full_sun and plant.full_shade:
        return "Full Sun to Full Shade"
    elif plant.full_sun and plant.part_shade:
        return "Full Sun to Part Shade"
    elif plant.part_shade and plant.full_shade:
        return "Part Shade to Full Shade"
    elif plant.full_sun:
        return "Full Sun"
    elif plant.part_shade:
        return "Part Shade"
    elif plant.full_shade:
        return "Full Shade"
    return "Unknown Light Range"


def plant_moisture_range(plant: PlantProfile):
    if plant.moisture_dry and plant.moisture_wet:
        return "Dry to Wet"
    elif plant.moisture_dry and plant.moisture_medium:
        return "Dry to Medium"
    elif plant.moisture_medium and plant.moisture_wet:
        return "Medium to Wet"
    elif plant.moisture_dry:
        return "Dry"
    elif plant.moisture_medium:
        return "Medium"
    elif plant.moisture_wet:
        return "Wet"
    return "Unknown Moisture Range"


def plant_sowing_notes(plant: PlantProfile):
    if plant.sowing_notes:

        note_list = plant.sowing_notes.split(".")
        note_list = [note.strip() for note in note_list if note.strip()]
        return note_list
    return []


def plant_label_info(plant: PlantProfile, request: HttpRequest) -> list[str]:
    double_dormancy = None
    latin_name = plant.latin_name
    english_name = plant.english_name
    french_name = plant.french_name
    light_range = plant_light_range(plant)
    moisture_range = f"Moisture: {plant_moisture_range(plant)}"
    plant_size = f"{str(plant.max_height)}' tall, {str(plant.max_width)}' wide"
    bloom_period = f"Bloom: {MONTHS.get(plant.bloom_start, '')} - {MONTHS.get(plant.bloom_end, '')}"
    sowing_notes = plant_sowing_notes(plant)
    sowing_time = sow_before(plant)
    sowing_depth = plant.sowing_depth.sowing_depth

    if plant.double_dormancy:
        double_dormancy = "Double Dormancy"

    label_info = [
        latin_name,
        english_name,
        french_name,
        light_range,
        moisture_range,
        plant_size,
        bloom_period,
        *sowing_notes,  # Unpack the list items individually
    ]

    if sowing_time:
        label_info.append(sowing_time)

    if sowing_depth:
        label_info.append(sowing_depth)

    _stratification_need = stratification_need(plant)
    if _stratification_need:
        label_info.append(_stratification_need)

    if double_dormancy:
        label_info.append(double_dormancy)

    label_info.reverse()
    return label_info


def stratification_need(plant: PlantProfile):
    # consider plant.stratification_detail and plant.stratification_duration and return appropriate string
    stratification_detail = None
    stratification_duration = None

    if plant.stratification_detail:
        stratification_detail = plant.stratification_detail
    if plant.stratification_duration:
        stratification_duration = plant.stratification_duration.__str__()

    if stratification_detail and stratification_duration:
        return f"{stratification_detail} {stratification_duration}"
    elif stratification_detail:
        return stratification_detail
    elif stratification_duration:
        return f"Stratify for {stratification_duration}"
    return None


def sow_before(plant: PlantProfile):
    if not plant.stratification_duration:
        return "Sow anytime"
    duration = plant.stratification_duration.stratification_duration
    if not duration or duration == 0:
        return "Sow anytime"
    if duration == 30:
        return "Sow by March"
    elif duration == 60:
        return "Sow by February"
    elif duration == 90:
        return "Sow by January"
    elif duration == 120:
        return "Sow by December"
    elif duration == 180:
        return "Sow by November"
    else:
        return None


def is_plant_toxic(plant: PlantProfile):
    """Check if a plant is toxic based on its toxicity indicator."""
    not_toxic_options = ["Not known to be toxic", "Unknown", "None", ""]
    return str(plant.toxicity_indicator) not in not_toxic_options


def get_plants_without_images():
    # Returns a queryset of PlantProfile instances without associated PlantImage entries.
    return PlantProfile.all_objects.filter(images__isnull=True)


def is_valid_url(url: str) -> bool:
    """Check if a given string is a valid URL."""
    from django.core.exceptions import ValidationError
    from django.core.validators import URLValidator

    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


def get_image_gps_coordinates(image_path: Path) -> dict | None:
    try:
        with open(image_path, "rb") as img_f:
            img = Image(img_f)
            if img.has_exif:
                if hasattr(img, "gps_latitude") and hasattr(img, "gps_longitude"):

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

                    return {
                        "latitude": lat_decimal,
                        "longitude": lon_decimal,
                    }

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {image_path}")
    except Exception:
        raise Exception(f"Error processing file {image_path}")

    return None


def flush_gps_coordinates(image_path: Path) -> dict | None:

    gps_coordinates = get_image_gps_coordinates(image_path)
    if not gps_coordinates:
        return None

    try:
        with open(image_path, "rb") as img_f:
            img = Image(img_f)
            if hasattr(img, "gps_latitude"):
                del img.gps_latitude

            if hasattr(img, "gps_longitude"):
                del img.gps_longitude

            if hasattr(img, "gps_latitude_ref"):
                del img.gps_latitude_ref

            if hasattr(img, "gps_longitude_ref"):
                del img.gps_longitude_ref

        with open(image_path, "wb") as new_img_f:
            new_img_f.write(img.get_file())

    except Exception:
        raise Exception(f"Error processing file {image_path}")

    return gps_coordinates


def create_qr_code(data: str, box_size: int = 10, border: int = 4):
    # createn a QR code and return as a base64 string
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def create_qr_code_image(data: str, box_size: int = 10, border: int = 4):
    # create a QR code and return as a PIL Image
    # good for direct embedding in PDFs
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img
