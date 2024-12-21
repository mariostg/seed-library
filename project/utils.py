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
    plant.bloom_start = MONTHS[plant.bloom_start]
    plant.bloom_end = MONTHS[plant.bloom_end]
    if plant.harvesting_end == plant.harvesting_start:
        plant.harvesting_end = None

    plant.harvesting_start = MONTHS[plant.harvesting_start]
    plant.harvesting_end = MONTHS[plant.harvesting_end]
    return plant
