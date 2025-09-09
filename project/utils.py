from django.http import HttpRequest

from project.models import PlantProfile

MONTHS = {
    0: "",
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
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


def plant_label_info(pk, request: HttpRequest):
    detail = None
    plant = single_plant(pk, request)
    if not plant.stratification_detail:
        plant.stratification_detail = "No Stratification"
    if plant.double_dormancy:
        detail = "Double Dormancy"
    label_info = [
        plant.latin_name,
        plant.english_name,
        plant.french_name,
        str(plant.max_height) + " feet",
        f"Bloom: {plant.bloom_start} - {plant.bloom_end}",
        plant.stratification_detail,
        plant.sowing_depth.sowing_depth,
    ]
    if detail:
        label_info.append(detail)
    label_info.reverse()
    return label_info


def sow_before(plant: PlantProfile):
    if not plant.stratification_duration:
        return "Sow anytime"
    if plant.stratification_duration == 30:
        return "Sow before March"
    elif plant.stratification_duration == 60:
        return "Sow before February"
    elif plant.stratification_duration == 90:
        return "Sow before January"
    elif plant.stratification_duration == 120:
        return "Sow before December"
    elif plant.stratification_duration == 180:
        return "Sow before November"


def is_plant_toxic(plant: PlantProfile):
    """Check if a plant is toxic based on its toxicity indicator."""
    not_toxic_options = ["Not known to be toxic", "Unknown", "None", ""]
    return str(plant.toxicity_indicator) not in not_toxic_options
