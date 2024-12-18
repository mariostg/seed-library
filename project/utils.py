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


def search_plants(request):

    search_criterion = {
        "english_name": "",
        "french_name": "",
        "latin_name": "",
        "light_from": "",
        "light_to": "",
        "bloom_start": None,
        "bloom_end": None,
        "soil_humidity_min": "",
        "soil_humidity_max": "",
        "max_height": "",
        "stratification_duration": 0,
        "sharing_priority": "",
        "harvesting_start": 0,
        "harvesting_end": 0,
        "germinate_easy": "unknown",
        "seed_availability": "unknown",
    }
    dataset = PlantProfile.objects.all()

    if not request.GET:
        return {}, search_criterion

    # Nomenclature

    if request.GET.get("english_name"):
        search_criterion["english_name"] = request.GET.get("english_name")
        dataset = dataset.filter(
            english_name__contains=search_criterion["english_name"],
        )

    if request.GET.get("french_name"):
        search_criterion["french_name"] = request.GET.get("french_name")
        dataset = dataset.filter(
            french_name__contains=search_criterion["french_name"],
        )

    if request.GET.get("latin_name"):
        search_criterion["latin_name"] = request.GET.get("latin_name")
        dataset = dataset.filter(
            latin_name__contains=search_criterion["latin_name"],
        )

    # Sun requirement

    if request.GET.get("light_from"):
        search_criterion["light_from"] = request.GET.get("light_from")

    if request.GET.get("light_to"):
        search_criterion["light_to"] = request.GET.get("light_to")

    if search_criterion["light_from"] and search_criterion["light_to"]:
        dataset = dataset.filter(
            light_from=search_criterion["light_from"],
        )
        dataset = dataset.filter(
            light_to__gte=search_criterion["light_to"],
        )
    elif search_criterion["light_from"]:
        dataset = dataset.filter(
            light_from=search_criterion["light_from"],
        )
    elif search_criterion["light_to"]:
        dataset = dataset.filter(
            light_to__gte=search_criterion["light_to"],
        )

    # Soil Humidity

    if request.GET.get("soil_humidity_min"):
        search_criterion["soil_humidity_min"] = request.GET.get("soil_humidity_min")

    if request.GET.get("soil_humidity_max"):
        search_criterion["soil_humidity_max"] = request.GET.get("soil_humidity_max")

    if search_criterion["soil_humidity_min"] and search_criterion["soil_humidity_max"]:
        dataset = dataset.filter(
            soil_humidity_min=search_criterion["soil_humidity_min"],
        )
        dataset = dataset.filter(
            soil_humidity_max__gte=search_criterion["soil_humidity_max"],
        )
    elif search_criterion["soil_humidity_min"]:
        dataset = dataset.filter(
            soil_humidity_min=search_criterion["soil_humidity_min"],
        )
    elif search_criterion["soil_humidity_max"]:
        dataset = dataset.filter(
            soil_humidity_max__gte=search_criterion["soil_humidity_max"],
        )

    # Bloom period

    if request.GET.get("bloom_start"):
        search_criterion["bloom_start"] = request.GET.get("bloom_start")

    if request.GET.get("bloom_end"):
        search_criterion["bloom_end"] = request.GET.get("bloom_end")

    if search_criterion["bloom_start"]:
        dataset = dataset.filter(
            bloom_start=search_criterion["bloom_start"],
        )
        if search_criterion["bloom_end"]:
            dataset = dataset.filter(
                bloom_end=search_criterion["bloom_end"],
            )
        else:
            dataset = dataset.filter(
                bloom_end="0",
            )

    # Height
    if request.GET.get("max_height"):
        search_criterion["max_height"] = request.GET.get("max_height")

    if search_criterion["max_height"] != "":
        dataset = dataset.filter(
            max_height=search_criterion["max_height"],
        )

    # Stratification

    if request.GET.get("stratification_duration"):
        search_criterion["stratification_duration"] = request.GET.get("stratification_duration")
        if search_criterion["stratification_duration"] != "0":
            dataset = dataset.filter(
                stratification_duration=search_criterion["stratification_duration"],
            )

    # Sharing Priority
    if request.GET.get("sharing_priority"):
        search_criterion["sharing_priority"] = request.GET.get("sharing_priority")
        dataset = dataset.filter(
            sharing_priority=search_criterion["sharing_priority"],
        )

    # Harvesting

    if request.GET.get("harvesting_start"):
        search_criterion["harvesting_start"] = request.GET.get("harvesting_start")

    if request.GET.get("harvesting_end"):
        search_criterion["harvesting_end"] = request.GET.get("harvesting_end")

    if search_criterion["harvesting_start"]:
        dataset = dataset.filter(
            harvesting_start=search_criterion["harvesting_start"],
        )
        if search_criterion["harvesting_end"]:
            dataset = dataset.filter(
                harvesting_end=search_criterion["harvesting_end"],
            )

    # Easy to germinate
    if request.GET.get("germinate_easy"):
        options = {"true": True, "false": False, None: False, "unknown": None}
        germinate_easy = options[request.GET.get("germinate_easy")]
        search_criterion["germinate_easy"] = germinate_easy

        if germinate_easy is not None:
            dataset = dataset.filter(
                germinate_easy=germinate_easy,
            )

    # Seed Availability
    if request.GET.get("seed_availability"):
        options = {"true": True, "false": False, None: False, "unknown": None}
        seed_availability = options[request.GET.get("seed_availability")]
        search_criterion["seed_availability"] = seed_availability

        if seed_availability is not None:
            dataset = dataset.filter(
                seed_availability=seed_availability,
            )

    return dataset, search_criterion


def single_plant(pk):
    plant = PlantProfile.objects.get(pk=pk)
    plant.bloom_start = MONTHS[plant.bloom_start]
    plant.bloom_end = MONTHS[plant.bloom_end]
    if plant.harvesting_end == plant.harvesting_start:
        plant.harvesting_end = None

    plant.harvesting_start = MONTHS[plant.harvesting_start]
    plant.harvesting_end = MONTHS[plant.harvesting_end]
    return plant
