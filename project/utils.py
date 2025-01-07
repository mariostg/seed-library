from project.models import PlantProfile

MONTHS = {
    None: "",
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


def single_plant(pk):
    plant = PlantProfile.objects.get(pk=pk)
    plant.bloom_start = MONTHS.get(plant.bloom_start, "")
    plant.bloom_end = MONTHS.get(plant.bloom_end, "")
    if plant.harvesting_end == plant.harvesting_start:
        plant.harvesting_end = None

    plant.harvesting_start = MONTHS[plant.harvesting_start]
    plant.harvesting_end = MONTHS[plant.harvesting_end]
    return plant


def plant_label_info(pk):
    plant = single_plant(pk)
    if not plant.stratification_detail:
        plant.stratification_detail = "No Stratification"
    if plant.dormancy.dormancy:
        detail = plant.dormancy.dormancy
    label_info = [
        plant.latin_name,
        plant.english_name,
        plant.french_name,
        f"{plant.light_from.lighting} - {plant.light_to.lighting}",
        f"Moisture: {plant.soil_humidity_min.soil_humidity} - {plant.soil_humidity_max.soil_humidity}",
        plant.size,
        f"Bloom: {plant.bloom_start} - {plant.bloom_end}",
        plant.stratification_detail,
        plant.sowing_depth.sowing_depth,
        detail,
    ]
    label_info.reverse()
    return label_info
