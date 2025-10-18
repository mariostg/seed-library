from django.http import HttpRequest

from project.models import PlantProfile

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
    detail = None

    if not plant.stratification_detail:
        plant.stratification_detail = "No Stratification"
    if plant.double_dormancy:
        detail = "Double Dormancy"
    label_info = [
        plant.latin_name,
        plant.english_name,
        plant.french_name,
        plant_light_range(plant),
        f"Moisture: {plant_moisture_range(plant)}",
        f"{str(plant.max_height)}' tall, {str(plant.max_width)}' wide",
        f"Bloom: {MONTHS.get(plant.bloom_start, '')} - {MONTHS.get(plant.bloom_end, '')}",
        *plant_sowing_notes(plant),  # Unpack the list items individually
        sow_before(plant),
        f"{plant.stratification_duration} days",
        plant.sowing_depth.sowing_depth,
    ]
    if detail:
        label_info.append(detail)
    label_info.reverse()
    return label_info


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
