import csv
import io

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import RestrictedError
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from reportlab.lib.colors import black, pink, red
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from project import filters, forms, models, utils, vascan
from project.models import ProjectUser


# Create your views here.
def index(request):
    return render(request, "project/plant-catalogue-intro.html")


@login_required
def toggle_availability(request, pk):
    plant = utils.single_plant(pk, request)
    plant.seed_availability = not plant.seed_availability
    plant.save()
    plant = utils.single_plant(pk, request)
    context = {"pk": plant.pk, "availability": plant.seed_availability}
    return JsonResponse(context)
    # return render(request, "project/update-availability.html", context)


def plant_profile_page(request, pk):
    plant: models.PlantProfile = utils.single_plant(pk, request)
    if not plant:
        return render(request, "core/404.html", status=404)
    is_row_garden = plant.boulevard_garden_tolerant and plant.max_height <= 2
    landscape_use = (
        # garden_suitability
        plant.container_suitable
        or plant.rain_garden
        or plant.rock_garden
        or plant.school_garden
        or plant.shoreline_rehab
        or plant.wetland_garden
        or plant.woodland_garden
        # functional_use
        or plant.ground_cover
        or plant.hedge
        or is_row_garden
    )
    ecological_benefits = (
        # wildlife_interaction
        plant.bird_friendly
        or plant.bee_host
        or plant.butterfly_host
        or plant.nitrogen_fixer
        or plant.keystones_species
    )
    bloom_start = utils.MONTHS[plant.bloom_start]
    bloom_end = utils.MONTHS[plant.bloom_end]
    sow_before = utils.sow_before(plant)
    is_toxic = utils.is_plant_toxic(plant)
    # !This will need to be refactored by including a boolean field in the ConservationStatus model
    endangered_values = (
        "Critically Imperiled",
        "Presumed Extirpated",
        "Imperiled",
        "Vulnerable",
    )

    if plant.conservation_status:
        endangered = plant.conservation_status.conservation_status in endangered_values
    else:
        endangered = False

    # check if plant video link is a valid url
    is_valid_video_url = utils.is_valid_url(plant.harvesting_video_link)
    if not is_valid_video_url:
        plant.harvesting_video_link = ""
    context = {
        "plant": plant,
        "title": plant.latin_name,
        "bloom_start": bloom_start,
        "bloom_end": bloom_end,
        "landscape_use": landscape_use,
        "is_row_garden": is_row_garden,
        "ecological_benefits": ecological_benefits,
        "sow_before": sow_before,
        "is_toxic": is_toxic,
        "endangered": endangered,
    }
    return render(request, "project/plant-profile-page.html", context)


# @login_required
def plant_profile_add(request):
    context = {
        "title": "Create Plant Profile",
        "url_name": "index",
    }
    if request.method == "POST":
        form = forms.PlantProfileForm(request.POST)
        if form.is_valid():
            context["form"] = form
            vascan_result = utils.vascan_query(form.cleaned_data["latin_name"])
            taxon_id = utils.extract_taxon_id(vascan_result)

            obj: models.PlantProfile = form.save(commit=False)
            obj.taxon = taxon_id
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Plant {obj.latin_name} exists already.")
                return render(
                    request,
                    "project/plant-profile-form.html",
                    context,
                )
            except ValueError as e:
                messages.error(request, e)
        else:
            messages.error(request, "Plant Profile not valid.")
            context["form"] = form
    else:
        context["form"] = forms.PlantProfileForm
    return render(request, "project/plant-profile-form.html", context)


# @login_required
def plant_profile_update(request, pk):
    context = {
        "title": "Update Plant Profile",
        "url_name": "index",
    }
    obj = utils.single_plant(pk, request)
    context["form"] = forms.PlantProfileForm(instance=obj)
    if request.method == "POST":
        form = forms.PlantProfileForm(request.POST, instance=obj)
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("plant-profile-page", pk=obj.pk)
    return render(request, "project/plant-profile-form.html", context)


# @login_required
def plant_profile_delete(request, pk):
    plant: models.PlantProfile = utils.single_plant(pk, request)
    if request.method == "POST":
        try:
            plant.delete()
        except RestrictedError:
            messages.info(
                request,
                f"Plant Profile {plant.latin_name} ne peut-être effacée car il existe des éléments associés.",
            )
        return redirect("search-plant-name")
    context = {"data": plant, "back": "plant-profile-page", "pk": plant.pk}
    return render(request, "core/delete-object.html", context)


def plant_catalogue_intro(request):
    context = {
        "title": "Plant Catalogue Introduction",
        "url_name": "plant-catalogue-intro",
    }
    return render(request, "project/plant_catalogue_intro.html", context)


def butterfly_supporting_plants(request):
    # This view is used to display a list of butterflies with the plants that support them
    butterflies = models.ButterflySpecies.objects.all().order_by("latin_name")
    context = {
        "title": "Butterfly Supporting Plants",
        "url_name": "butterfly-supporting-plants",
        "butterflies": butterflies,
    }
    return render(request, "project/butterfly_supporting_plants.html", context)


def bee_supporting_plants(request):
    # This view is used to display a list of bees with the plants that support them
    bees = models.BeeSpecies.objects.all().order_by("latin_name")
    context = {
        "title": "Bee Supporting Plants",
        "url_name": "bee-supporting-plants",
        "bees": bees,
    }
    return render(request, "project/bee_supporting_plants.html", context)


def search_plant_name(request):
    if not request.GET:
        data = models.PlantProfile.objects.none()
    elif request.user.is_authenticated:
        data = models.PlantProfile.all_objects.all().order_by("latin_name")
    else:
        data = models.PlantProfile.objects.all().order_by("latin_name")

    object_list = filters.PlantProfileFilter(request.GET, queryset=data)
    ecozones = models.Ecozone.objects.all().order_by("ecozone")
    # Create lists of different filter categories
    sun_filters = [
        "#full_sun",
        "#part_shade",
        "#full_shade",
    ]
    moisture_filters = [
        "#moisture_dry",
        "#moisture_medium",
        "#moisture_wet",
    ]
    plant_type_filters = [
        "#flowering_plant",
        "#grass_sedge_rush",
        "#shrub",
        "#deciduous_tree",
        "#conifer_tree",
        "#vine",
    ]
    physical_attributes_filters = [
        "#max_height",
        "#max_width",
    ]
    lifecycle_filters = [
        "#annual",
        "#biennial",
        "#perennial",
        "#spring_ephemeral",
        "#self_seeding",
    ]
    bloom_period_filters = [
        "#bloom_start",
        "#bloom_end",
    ]
    colour_filters = [
        "#colour_blue",
        "#colour_green",
        "#colour_orange",
        "#colour_pink",
        "#colour_purple",
        "#colour_red",
        "#colour_white",
        "#colour_yellow",
    ]
    soil_tolerance_filters = [
        "#limestone_tolerant",
        "#sand_tolerant",
        "#acidic_soil_tolerant",
    ]

    harvesting_start_filters = [f"#harvesting_start_{month}" for month in range(4, 13)]
    seed_sharing_filters = [
        "#seed_availability",
        "#accepting_seed",
    ]
    garden_suitability_filters = [
        "#rock_garden",
        "#rain_garden",
        "#shoreline_rehab",
        "#container_suitable",
        "#school_garden",
        "#woodland_garden",
        "#wetland_garden",
        "#boulevard_garden_tolerant",
        "#row_garden",
    ]
    functional_use_filters = [
        "#ground_cover",
        "#hedge",
        "#windbreak_edge",
    ]
    gardening_experience_filters = [
        "#beginner_friendly",
        "#does_not_spread",
        "#transplantation_tolerant",
        "#germinate_easy",
        "#starter_pack_shade",
        "#starter_pack_sun_dry",
        "#starter_pack_sun_wet",
    ]
    wildlife_interaction_filters = [
        "#hummingbird_friendly",
        "#pollinator_garden",
        "#bird_friendly",
        "#deer_tolerant",
        "#rabbit_tolerant",
    ]
    environmental_stress_tolerance_filters = [
        "#drought_tolerant",
        "#salt_tolerant",
        "#foot_traffic_tolerant",
        "#juglone_tolerant",
    ]
    ecosystem_services_filters = [
        "#bee_host",
        "#butterfly_host",
        "#nitrogen_fixer",
        "#keystones_species",
    ]
    conservation_status_filters = [
        "#endangered",
        "#grasp_candidate",
        "#native_to_ottawa_region",
    ]
    safety_and_compatibility_filters = [
        "#septic_tank_safe",
        "#cause_skin_rashes",
        "#produces_burs",
        "#exclude_toxic",
    ]
    region_filters = [
        "#is_native_to_AB",
        "#is_native_to_BC",
        "#is_native_to_MB",
        "#is_native_to_NB",
        "#is_native_to_NL",
        "#is_native_to_NS",
        "#is_native_to_NT",
        "#is_native_to_NU",
        "#is_native_to_ON",
        "#is_native_to_PE",
        "#is_native_to_QC",
        "#is_native_to_SK",
        "#is_native_to_YT",
        "#native_to_ottawa_region",
    ]
    ecozones_filters = [f"#ecozone_{ecozone.id}" for ecozone in ecozones]
    admin_controls_filters = [
        "#is_draft",
        "#is_active",
        "#is_accepted",
        "#has_notice",
    ]

    # Merge all filter lists and join with commas
    hx_include = ",".join(
        ["#any_plant_name"]
        + ["#is_active"]
        + sun_filters
        + moisture_filters
        + plant_type_filters
        + physical_attributes_filters
        + lifecycle_filters
        + bloom_period_filters
        + colour_filters
        + soil_tolerance_filters
        + harvesting_start_filters
        + ["#stratification_duration"]
        + seed_sharing_filters
        + garden_suitability_filters
        + functional_use_filters
        + gardening_experience_filters
        + wildlife_interaction_filters
        + environmental_stress_tolerance_filters
        + ecosystem_services_filters
        + conservation_status_filters
        + safety_and_compatibility_filters
        + region_filters
        + ecozones_filters
        + admin_controls_filters
    )
    item_count = object_list.qs.count()
    stratification_durations = models.StratificationDuration.objects.all().order_by(
        "stratification_duration"
    )
    context = {
        "ecozones": ecozones,
        "stratification_durations": stratification_durations,
        "months": utils.MONTHS.values(),
        "months_numbered": utils.MONTHS.items(),
        "harvesting_period": {
            k: utils.MONTHS[k] for k in range(5, 12)
        },  # from April (index 3) to December (index 11)
        "object_list": object_list.qs,
        "url_name": "index",
        "title": "Plant Profile Filter",
        "item_count": item_count,
        "hx_include": hx_include,
    }
    template = (
        "project/plant-search-results.html"
        if request.htmx
        else "project/plant-catalog.html"
    )
    return render(request, template, context)


def search_vascan_taxon_id(request):
    # uses vascan.vascan_query and vascan.extract_taxon_id from an htmx request
    if request.method == "GET" and "latin_name" in request.GET:
        latin_name = request.GET["latin_name"]
        vascan_result = vascan.vascan_query(latin_name)
        taxon_id = vascan.extract_taxon_id(vascan_result)
        english_name = vascan.extract_english_name(vascan_result)
        french_name = vascan.extract_french_name(vascan_result)
        return HttpResponse(
            f"""
            <input id="id_taxon" value="{taxon_id}" hx-swap-oob="true">
            <input id="id_english_name" value="{english_name}" hx-swap-oob="true">
            <input id="id_french_name" value="{french_name}" hx-swap-oob="true">
        """
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


def export_plant_search_results(request):
    """
    Exports plant search results to a CSV file based on the provided request parameters.
    This view function handles the export of filtered plant profiles to a CSV format.
    It uses the request's GET parameters to filter the plant profiles and returns
    a HttpResponse with the CSV content.
    If no GET parameters are provided, an empty queryset is used.
    If the user is authenticated, all plant profiles (including inactive ones) are included.
    Otherwise, only active plant profiles are included.
    Parameters:
        request (HttpRequest): The HTTP request object containing GET parameters for filtering.
    Returns:
        HttpResponse: A response object with CSV content and appropriate headers
                      for the client to download as 'plant_search_results.csv'.
    CSV Fields Include:
        - Latin Name
        - English Name
        - French Name
        - Is Active (if user is authenticated)
        - Max Height(feet)
        - Max Width(feet)
        - Bloom Start
        - Bloom End
        - Bloom Colour
        - Full Sun
        - Part Shade
        - Full Shade
        - Moisture Dry
        - Moisture Medium
        - Moisture Wet
        - Lifespan
        - Plant Type
        - Soil acidic
        - Soil limestone
        - Soil sand
        - Harvesting Start
        - Seed Event Table
    """

    if not request.GET:
        data = models.PlantProfile.objects.none()
    elif request.user.is_authenticated:
        data = models.PlantProfile.all_objects.all().order_by("latin_name")
    else:
        data = models.PlantProfile.objects.all().order_by("latin_name")

    plant_profiles = filters.PlantProfileFilter(request.GET, queryset=data)
    # Create the CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="plant_search_results.csv"'
    writer = csv.writer(response)
    # Write the header row
    row_header = [
        "Latin Name",
        "English Name",
        "French Name",
        "Max Height(feet)",
        "Max Width(feet)",
        "Bloom Start",
        "Bloom End",
        "Bloom Colour",
        "Full Sun",
        "Part Shade",
        "Full Shade",
        "Moisture Dry",
        "Moisture Medium",
        "Moisture Wet",
        "Lifespan",
        "Plant Type",
        "Harvesting Start",
        "Seed Event Table",
        "Toxicity",
        "Harvesting Indicator",
        "Harvesting Mean",
        "Seed Viability Test",
        "Seed Storage",
        "Packaging Measure",
        "Stratification requirement",
        "Sowing Depth (inches)",
        "Plant Profile URL",
    ]
    if request.user.is_authenticated:
        row_header.insert(3, "Is Active")
    writer.writerow(row_header)
    # Write the data rows
    for plant in plant_profiles.qs:
        plant: (
            models.PlantProfile
        )  # Type hint for better IDE support and code readability
        row = [
            plant.latin_name,
            plant.english_name,
            plant.french_name,
            plant.max_height,
            plant.max_width,
            plant.bloom_start,
            plant.bloom_end,
            plant.bloom_colour,
            "Yes" if plant.full_sun else "No",
            "Yes" if plant.part_shade else "No",
            "Yes" if plant.full_shade else "No",
            "Yes" if plant.moisture_dry else "No",
            "Yes" if plant.moisture_medium else "No",
            "Yes" if plant.moisture_wet else "No",
            plant.lifespan,
            plant.growth_habit,
            plant.harvesting_start,
            plant.seed_event_table,
            plant.toxicity_indicator,
            plant.harvesting_indicator,
            plant.harvesting_mean,
            plant.seed_viability_test,
            plant.seed_storage,
            plant.packaging_measure,
            f"{plant.stratification_duration},{plant.stratification_detail}",
            plant.sowing_depth,
            request.build_absolute_uri(redirect("plant-profile-page", pk=plant.pk).url),
        ]
        if request.user.is_authenticated:
            row.insert(3, "Yes" if plant.is_active else "No")
        writer.writerow(row)
    return response


# @login_required
def update_availability(request):
    plants = utils.all_plants(request).order_by("seed_event_table", "latin_name")
    context = {"object_list": plants}
    return render(request, "project/update-availability.html", context)


def habit_table(request):
    data = models.GrowthHabit.objects.all().order_by("habit")
    context = {
        "data": data,
        "url_name": "habit-table",
        "title": "Habits",
    }
    return render(request, "project/habit-table.html", context)


def harvesting_indicator_table(request):
    data = models.HarvestingIndicator.objects.all().order_by("harvesting_indicator")
    context = {
        "data": data,
        "url_name": "harvesting-indicator-table",
        "title": "Harvesting Indicators",
    }
    return render(request, "project/harvesting-indicator-table.html", context)


def harvesting_mean_table(request):
    data = models.HarvestingMean.objects.all().order_by("harvesting_mean")
    context = {
        "data": data,
        "url_name": "harvesting-mean-table",
        "title": "Harvesting Means",
    }
    return render(request, "project/harvesting-mean-table.html", context)


def admin_colour_page(request):
    data = models.BloomColour.objects.all().order_by("bloom_colour")
    context = {
        "data": data,
        "url_name": "colour-page",
        "title": "Colours",
    }
    return render(request, "project/admin/admin-colour-page.html", context)


# @login_required
def admin_colour_add(request):
    context = {
        "title": "Create Colour",
        "url_name": "admin-colour-page",
    }
    if request.method == "POST":
        form = forms.AdminColourForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj: models.BloomColour = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Colour {obj.bloom_colour} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Color not valid.")
            context["form"] = form
    else:
        context["form"] = forms.AdminColourForm

    return render(request, "project/simple-form.html", context)


# @login_required
def admin_colour_update(request, pk):
    colour = models.BloomColour.objects.get(id=pk)
    form = forms.AdminColourForm(instance=colour)

    if request.method == "POST":
        form = forms.AdminColourForm(request.POST, instance=colour)
        if form.is_valid():
            form.save()
            return redirect("admin-colour-page")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Colour Update",
            "url_name": "admin-colour-page",
        },
    )


# @login_required
def admin_colour_delete(request, pk):
    obj: models.BloomColour = models.BloomColour.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.obj)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("admin-colour-page")
    context = {"object": obj, "back": "admin-colour-page"}
    return render(request, "core/delete-object.html", context)


# @login_required
def habit_add(request):
    context = {
        "title": "Create Habit",
        "url_name": "habit-table",
    }
    if request.method == "POST":
        form = forms.HabitForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Habit {obj.habit} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Habit not valid.")
            context["form"] = form
    else:
        context["form"] = forms.HabitForm

    return render(request, "project/simple-form.html", context)


# @login_required
def harvesting_indicator_add(request):
    context = {
        "title": "Create Harvesting Indicator",
        "url_name": "harvesting-indicator-table",
    }
    if request.method == "POST":
        form = forms.HarvestingIndicatorForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(
                    request,
                    f"Harvesting Indicator {obj.harvesting_indicator} exists already.",
                )
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Harvesting Indicator not valid.")
            context["form"] = form
    else:
        context["form"] = forms.HarvestingIndicatorForm

    return render(request, "project/simple-form.html", context)


# @login_required
def harvesting_mean_add(request):
    context = {
        "title": "Create Harvesting Mean Statement",
        "url_name": "harvesting-mean-table",
    }
    if request.method == "POST":
        form = forms.HarvestingMeanForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(
                    request, f"Harvesting Mean {obj.harvesting_mean} exists already."
                )
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Harvesting Mean not valid.")
            context["form"] = form
    else:
        context["form"] = forms.HarvestingMeanForm

    return render(request, "project/simple-form.html", context)


# @login_required
def habit_update(request, pk):
    obj = models.GrowthHabit.objects.get(id=pk)
    form = forms.HabitForm(instance=obj)

    if request.method == "POST":
        form = forms.ColorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("habit-table")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Habit Update",
            "url_name": "habit-table",
        },
    )


# @login_required
def harvesting_indicator_update(request, pk):
    obj = models.HarvestingIndicator.objects.get(id=pk)
    form = forms.HarvestingIndicatorForm(instance=obj)

    if request.method == "POST":
        form = forms.HarvestingIndicatorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("harvesting-indicator-table")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Harvesting Indicator Update",
            "url_name": "harvesting-indicator-table",
        },
    )


# @login_required
def harvesting_mean_update(request, pk):
    obj = models.HarvestingMean.objects.get(id=pk)
    form = forms.HarvestingMeanForm(instance=obj)

    if request.method == "POST":
        form = forms.HarvestingMeanForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("harvesting-mean-table")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Harvesting Mean Update",
            "url_name": "harvesting-mean-table",
        },
    )


# @login_required
def habit_delete(request, pk):
    obj: models.GrowthHabit = models.GrowthHabit.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.habit)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("habit-table")
    context = {"object": obj, "back": "habit-table"}
    return render(request, "core/delete-object.html", context)


# @login_required
def harvesting_indicator_delete(request, pk):
    obj: models.HarvestingIndicator = models.HarvestingIndicator.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.harvesting_indicator)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("harvesting-indicator-table")
    context = {"object": obj, "back": "harvesting-indicator-table"}
    return render(request, "core/delete-object.html", context)


# @login_required
def harvesting_mean_delete(request, pk):
    obj: models.HarvestingMean = models.HarvestingMean.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.harvesting_mean)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("harvesting-mean-table")
    context = {"object": obj, "back": "harvesting-mean-table"}
    return render(request, "core/delete-object.html", context)


####
# User
####


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = ProjectUser.objects.get(username=username)
        except ProjectUser.DoesNotExist:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                request.GET["next"] if "next" in request.GET else "site-admin"
            )
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "project/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def user_plant_collection(request):
    obj = models.PlantCollection.objects.filter(owner=request.user)

    context = {"object_list": obj}
    return render(request, "project/plant-collection.html", context)


# @login_required
def user_plant_update(request, pk):
    obj = models.PlantCollection.objects.get(id=pk)
    if obj.owner != request.user:
        messages.warning(request, "You are not allowed to modify this user plant")
    form = forms.PlantCollectionForm(instance=obj)

    if request.method == "POST":
        form = forms.PlantCollectionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("user-plant-collection")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Color Update",
            "url_name": "user-plant-collection",
        },
    )


@login_required
def user_plant_toggle(request, pk):
    plant = utils.single_plant(pk, request)
    user = None
    if request.user.is_authenticated:
        user = request.user
        try:
            user_plant = models.PlantCollection.objects.get(owner=user, plants=plant)
            user_plant.delete()
            user_plant = None
            isowner = "No"
            td_class = "toggler crossmark"
        except models.PlantCollection.DoesNotExist:
            user_plant = models.PlantCollection(owner=user, plants=plant)
            user_plant.save()
            isowner = "Yes"
            td_class = "toggler checkmark"
    context = {"isowner": isowner, "plant_pk": plant.pk, "td_class": td_class}
    return JsonResponse(context)


@login_required
def user_plant_delete(request, pk):
    obj: models.PlantCollection = models.PlantCollection.objects.get(id=pk)
    if obj.owner != request.user:
        messages.warning(
            request, "You are not allowed to delete this plant from the user collection"
        )
        return render(request, "project/user-plant-collection.html")
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.habit)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("user-plant-collection")
    context = {"object": obj, "back": "user-plant-collection"}
    return render(request, "core/delete-object.html", context)


@login_required
def plant_collection_csv(request):
    data = models.PlantProfile.objects.filter(plantcollection__owner=request.user)

    fields = [field.name for field in data.model._meta.fields]
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="plant-collection.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in data:
        writer.writerow([getattr(obj, field) for field in fields])
    return response


# @login_required
def siteadmin(request):
    return render(request, "project/admin/admin.html")


def plant_label_pdf(request, pk):
    plant = utils.single_plant(pk, request)
    plant_info: list[str] = utils.plant_label_info(plant, request)
    plant_info_len = len(plant_info)
    plant_longest_string = max(plant_info, key=len)
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    c.setStrokeColor(pink)

    label_width = len(plant_longest_string) * 0.06818  # 1.5
    label_margin_x = 0.1
    label_margin_y = 0.1
    line_spacing = 0.155
    label_height = plant_info_len * line_spacing + line_spacing
    y_range = int(8.5 / label_height) + 1
    x_positions = [label_margin_x * inch * label_width]
    counter = 1
    while x_positions[-1] + (label_margin_x + label_width) * inch < 11 * inch:
        x_positions.append(
            (label_margin_x + label_width * counter + label_margin_x) * inch
        )
        counter += 1
    y_positions = [(y_ + label_margin_y) * inch * label_height for y_ in range(y_range)]

    c.grid(x_positions, y_positions)
    c.setStrokeColor(black)
    c.setFont("Times-Roman", 10)

    def draw_plant_info(
        c, x_position, y_position, label_margin_x, label_margin_y, line_spacing, info
    ):
        for idx, text in enumerate(info):
            xpos = x_position + label_margin_x * inch
            ypos = y_position + (label_margin_y + line_spacing * idx) * inch
            c.drawString(xpos, ypos, text)

    for x in range(len(x_positions) - 1):
        for y in range(y_range - 1):
            draw_plant_info(
                c,
                x_positions[x],
                y_positions[y],
                label_margin_x,
                label_margin_y,
                line_spacing,
                plant_info,
            )

    c.setFillColor(red)

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename=f"{plant.latin_name.replace(' ', '_')}.pdf"
    )


def plant_catalog(request):
    plants = models.PlantProfile.objects.none()
    context = {
        "title": "Plant Catalog",
        "object_list": plants,
        "url_name": "plant-catalog",
    }
    return render(request, "project/plant-catalog.html", context)


# View to update plant profile characteristics


@login_required
# update the environmental requirements of a plant profile if there is a post request
def plant_environmental_requirement_update(request, pk):
    plant = utils.single_plant(pk, request)
    if request.method == "POST":
        plant.full_sun = request.POST.get("full_sun") == "on"
        plant.part_shade = request.POST.get("part_shade") == "on"
        plant.full_shade = request.POST.get("full_shade") == "on"
        plant.moisture_dry = request.POST.get("moisture_dry") == "on"
        plant.moisture_medium = request.POST.get("moisture_medium") == "on"
        plant.moisture_wet = request.POST.get("moisture_wet") == "on"
        plant.limestone_tolerant = request.POST.get("limestone_tolerant") == "on"
        plant.sand_tolerant = request.POST.get("sand_tolerant") == "on"
        plant.acidic_soil_tolerant = request.POST.get("acidic_soil_tolerant") == "on"
        plant.save()
        messages.success(request, "Environmental requirements updated successfully.")
        return redirect("plant-profile-page", pk=plant.pk)
    context = {
        "title": f"{plant.latin_name} - Environmental Requirements",
        "plant": plant,
    }
    return render(
        request, "project/plant-environmental-requirement-update.html", context
    )


@login_required
def plant_identification_information_update(request, pk):
    plant = utils.single_plant(pk, request)
    context = {
        "title": f"{plant.latin_name} - Identification Information",
        "plant": plant,
    }
    if request.method == "POST":
        form = forms.PlantIdentificationInformationForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Identification information updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating identification information.")
    return render(
        request, "project/plant-identification-information-update.html", context
    )


def plant_identification_information_create(request):
    context = {
        "title": "Create Plant Identification Information",
    }
    if request.method == "POST":
        form = forms.PlantIdentificationInformationForm(request.POST)
        if form.is_valid():
            # Check if the plant already exists and if so, return message error
            latin_name = form.cleaned_data["latin_name"].capitalize()

            if models.PlantProfile.objects.filter(latin_name=latin_name).exists():
                messages.error(
                    request,
                    f"A plant with this Latin name {latin_name} already exists. Please choose a different name.",
                )
                return render(
                    request,
                    "project/plant-identification-information-create.html",
                    context,
                )

            context["form"] = form
            vascan_result = vascan.vascan_query(form.cleaned_data["latin_name"])
            taxon_id = vascan.extract_taxon_id(vascan_result)
            english_name = vascan.extract_english_name(vascan_result)
            french_name = vascan.extract_french_name(vascan_result)

            plant: models.PlantProfile = form.save(commit=False)
            plant.taxon = taxon_id
            plant.english_name = english_name
            plant.french_name = french_name
            plant.save()
            messages.success(
                request, "Plant identification information created successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
    else:
        form = forms.PlantIdentificationInformationForm()
    context = {
        "title": "Create Plant Identification Information",
        "form": form,
    }
    return render(
        request, "project/plant-identification-information-create.html", context
    )


def plant_growth_characteristics_update(request, pk):
    plant: models.PlantProfile = utils.single_plant(pk, request)
    plants_complements = models.PlantComplementary.objects.filter(plant_profile_id=pk)
    plants = models.PlantProfile.all_objects.exclude(
        pk__in=[p.complement_id for p in plants_complements]
    )
    growth_habits = models.GrowthHabit.objects.all().order_by("growth_habit")
    lifespan_choices = models.PlantLifespan.objects.all().order_by("lifespan")
    bloom_colours = models.BloomColour.objects.all().order_by("bloom_colour")
    bloom_starts = bloom_ends = utils.MONTHS
    context = {
        "title": f"{plant.latin_name} - Growth Characteristics",
        "plant": plant,
        "growth_habits": growth_habits,
        "bloom_colours": bloom_colours,
        "bloom_starts": bloom_starts,
        "bloom_ends": bloom_ends,
        "lifespan_choices": lifespan_choices,
        "plants": plants,
        "plant_complements": plants_complements,
    }

    if request.method == "POST":
        form = forms.PlantGrowthCharacteristicsForm(request.POST, instance=plant)
        if form.is_valid():
            # Get the plant complements from the form
            form.save()

            # Clear existing complements
            models.PlantComplementary.objects.filter(plant_profile=plant).delete()

            # Add new complements from the form data
            complement_ids = request.POST.getlist("complements")
            if complement_ids:
                for complement_id in complement_ids:
                    try:
                        complement_plant = models.PlantProfile.objects.get(
                            pk=complement_id
                        )
                        try:
                            models.PlantComplementary.objects.create(
                                plant_profile=plant, complement=complement_plant
                            )
                        except IntegrityError:
                            messages.warning(
                                request,
                                f"Complementary plant ID {complement_id} already exists.",
                            )
                    except models.PlantProfile.DoesNotExist:
                        messages.warning(
                            request,
                            f"Complementary plant ID {complement_id} not found.",
                        )
            messages.success(request, "Growth characteristics updated successfully.")
            return redirect("plant-profile-page", pk=plant.pk)
    else:
        form = forms.PlantGrowthCharacteristicsForm(instance=plant)
    return render(request, "project/plant-growth-characteristics-update.html", context)


def plant_landscape_use_and_application_update(request, pk):
    plant = utils.single_plant(pk, request)
    context = {
        "title": f"{plant.latin_name} - Landscape Use and Application",
        "plant": plant,
    }
    if request.method == "POST":
        form = forms.PlantLandscapeUseAndApplicationForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Landscape use and application updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating landscape use and application.")
    else:
        form = forms.PlantLandscapeUseAndApplicationForm(instance=plant)
    context["form"] = form
    return render(
        request, "project/plant-landscape-use-and-application-update.html", context
    )


def plant_ecological_benefits_update(request, pk):
    plant = utils.single_plant(pk, request)
    unsupported_butterflies = models.ButterflySpecies.objects.exclude(
        pk__in=plant.butterflies.all()
    )
    unsupported_bees = models.BeeSpecies.objects.exclude(pk__in=plant.bees.all())
    context = {
        "title": f"{plant.latin_name} - Ecological Benefits",
        "plant": plant,
        "unsupported_butterflies": unsupported_butterflies,
        "unsupported_bees": unsupported_bees,
    }
    if request.method == "POST":
        form = forms.PlantEcologicalBenefitsForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, "Ecological benefits updated successfully.")
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating ecological benefits.")
    else:
        form = forms.PlantEcologicalBenefitsForm(instance=plant)
    context["form"] = form
    return render(request, "project/plant-ecological-benefits-update.html", context)


def plant_introductory_gardening_experience_update(request, pk):
    plant = utils.single_plant(pk, request)
    context = {
        "title": f"{plant.latin_name} - Introductory Gardening Experience",
        "plant": plant,
    }
    if request.method == "POST":
        form = forms.PlantIntroductoryGardeningExperienceForm(
            request.POST, instance=plant
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "Introductory gardening experience updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating introductory gardening experience.")
    else:
        form = forms.PlantIntroductoryGardeningExperienceForm(instance=plant)
    context["form"] = form
    return render(
        request,
        "project/plant-introductory-gardening-experience-update.html",
        context,
    )


def plant_special_features_and_consideration_update(request, pk):
    plant = utils.single_plant(pk, request)
    context = {
        "title": f"{plant.latin_name} - Special Features and Considerations",
        "plant": plant,
    }
    if request.method == "POST":
        form = forms.PlantSpecialFeaturesAndConsiderationForm(
            request.POST, instance=plant
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "Special features and considerations updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(
                request, "Error updating special features and considerations."
            )
    else:
        form = forms.PlantSpecialFeaturesAndConsiderationForm(instance=plant)
    context["form"] = form

    ecozones = models.Ecozone.objects.all().order_by("ecozone")
    context["ecozones"] = ecozones

    ecozones_ids = plant.ecozones.values_list("id", flat=True)
    context["ecozones_ids"] = ecozones_ids
    return render(
        request,
        "project/plant-special-features-and-considerations-update.html",
        context,
    )


def plant_harvesting_update(request, pk):
    plant = utils.single_plant(pk, request)
    harvesting_months = utils.MONTHS
    # packaging measures
    # packaging_measures = models.PackagingMeasure.objects.all().order_by(
    #     "packaging_measure"
    # )
    # if not packaging_measures:
    #     messages.warning(
    #         request, "No packaging measures available. Please add some first."
    #     )
    #     return redirect("packaging-measure-table")

    # On Cultivars
    on_cultivars = models.OneCultivar.objects.all().order_by("on_cultivar")
    if not on_cultivars:
        messages.warning(request, "No on cultivars available. Please add some first.")
        return redirect("on-cultivar-table")

    # # Seed Viability Tests
    # seed_viability_tests = models.SeedViabilityTest.objects.all().order_by(
    #     "seed_viability_test"
    # )
    # if not seed_viability_tests:
    #     messages.warning(
    #         request, "No seed viability tests available. Please add some first."
    #     )
    #     return redirect("seed-viability-test-table")

    # Seed Storage
    seed_storages = models.SeedStorage.objects.all().order_by("seed_storage")
    if not seed_storages:
        messages.warning(
            request, "No seed storage options available. Please add some first."
        )
        return redirect("seed-storage-table")

    # harvesting indicators
    harvesting_indicators = models.HarvestingIndicator.objects.all().order_by(
        "harvesting_indicator"
    )
    if not harvesting_indicators:
        messages.warning(
            request, "No harvesting indicators available. Please add some first."
        )
        return redirect("harvesting-indicator-table")

    # harvesting means
    harvesting_means = models.HarvestingMean.objects.all().order_by("harvesting_mean")
    if not harvesting_means:
        messages.warning(
            request, "No harvesting means available. Please add some first."
        )
        return redirect("harvesting-mean-table")

    # # seed heads
    seed_heads = models.SeedHead.objects.all().order_by("seed_head")
    if not seed_heads:
        messages.warning(request, "No seed heads available. Please add some first.")
        return redirect("seed-head-table")

    # seed viability tests
    seed_viability_tests = models.SeedViabilityTest.objects.all().order_by(
        "seed_viability_test"
    )
    if not seed_viability_tests:
        messages.warning(
            request, "No seed viability tests available. Please add some first."
        )
        return redirect("seed-viability-test-table")

    # # seed event table
    # seed_event_table = models.SeedEventTable.objects.all().order_by("seed_event_table")
    # if not seed_event_table:
    #     messages.warning(
    #         request,
    #         "No seed event table available for this plant. Please add some first.",
    #     )
    #     return redirect("seed-event-table-table")

    if request.method == "POST":
        form = forms.PlantHarvestingForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Harvesting and seed sharing updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating harvesting and seed sharing.")
    else:
        form = forms.PlantHarvestingForm(instance=plant)

    context = {
        "title": f"{plant.latin_name} - Harvesting and Seed Sharing",
        "plant": plant,
        # "packaging_measures": packaging_measures,
        "on_cultivars": on_cultivars,
        "seed_viability_tests": seed_viability_tests,
        "seed_storages": seed_storages,
        # "sowing_depth": sowing_depth,
        "harvesting_months": harvesting_months,
        "harvesting_indicators": harvesting_indicators,
        "harvesting_means": harvesting_means,
        "seed_heads": seed_heads,
        # "seed_event_table": seed_event_table,
    }
    return render(request, "project/plant-harvesting-update.html", context)


def plant_sowing_update(request, pk):
    plant = utils.single_plant(pk, request)

    # sowing depth
    sowing_depth = models.SowingDepth.objects.all().order_by("sowing_depth")
    if not sowing_depth:
        messages.warning(request, "No sowing depth available. Please add some first.")
        return redirect("sowing-depth-table")

    if request.method == "POST":
        form = forms.PlantSowingForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, "Sowing information updated successfully.")
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating sowing information.")
    else:
        form = forms.PlantSowingForm(instance=plant)

    context = {
        "title": f"{plant.latin_name} - Sowing Information",
        "plant": plant,
        "sowing_depth": sowing_depth,
        "form": form,
    }
    return render(request, "project/plant-sowing-update.html", context)


def plant_seed_distribution_update(request, pk):
    plant = utils.single_plant(pk, request)

    if request.method == "POST":
        form = forms.PlantSeedDistributionForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Seed distribution information updated successfully."
            )
            return redirect("plant-profile-page", pk=plant.pk)
        else:
            messages.error(request, "Error updating seed distribution information.")
    else:
        form = forms.PlantSeedDistributionForm(instance=plant)

    context = {
        "title": f"{plant.latin_name} - Seed Distribution Information",
        "plant": plant,
        "form": form,
    }
    return render(request, "project/plant-seed-distribution-update.html", context)


def plant_ecozones(request):
    # export a csv file of all plants with their ecozones.
    # the first row is the header with the ecozone names.
    # the first column is the latin name.
    # other columns are the ecozones, with a 1 if the plant is in that ecozone, 0 otherwise.
    plants = models.PlantProfile.objects.all().order_by("latin_name")
    ecozones = models.Ecozone.objects.all().order_by("ecozone")
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="plant-ecozones.csv"'},
    )
    writer = csv.writer(response)
    header = ["Latin Name"] + [ecozone.ecozone for ecozone in ecozones]
    writer.writerow(header)
    for plant in plants:
        row = [plant.latin_name]
        plant_ecozones = plant.ecozones.values_list("ecozone", flat=True)
        for ecozone in ecozones:
            if ecozone.ecozone in plant_ecozones:
                row.append(1)
            else:
                row.append(0)
        writer.writerow(row)
    return response


@login_required
def admin_lifespan_page(request):
    obj = models.PlantLifespan.objects.all().order_by("lifespan")
    context = {
        "title": "Plant Lifespan",
        "object_list": obj,
        "url_name": "admin-lifespan-page",
    }
    return render(request, "project/admin/admin-lifespan-page.html", context)


@login_required
def admin_lifespan_add(request):
    context = {
        "title": "Create Plant Lifespan",
        "url_name": "admin-lifespan-page",
    }
    if request.method == "POST":
        form = forms.AdminLifespanForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Lifespan {obj.lifespan} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Lifespan not valid.")
            context["form"] = form
    else:
        context["form"] = forms.AdminLifespanForm()

    return render(request, "project/simple-form.html", context)


@login_required
def admin_lifespan_update(request, pk):
    obj = models.PlantLifespan.objects.get(id=pk)
    form = forms.AdminLifespanForm(instance=obj)

    if request.method == "POST":
        form = forms.AdminLifespanForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("admin-lifespan-page")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Lifespan Update",
            "url_name": "admin-lifespan-page",
        },
    )


@login_required
def admin_lifespan_delete(request, pk):
    obj: models.PlantLifespan = models.PlantLifespan.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.lifespan)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("admin-lifespan-page")
    context = {"object": obj, "back": "admin-lifespan-page"}
    return render(request, "core/delete-object.html", context)


@login_required
def admin_growth_habit_page(request):
    obj = models.GrowthHabit.objects.all().order_by("growth_habit")
    context = {
        "title": "Growth Habit",
        "object_list": obj,
        "url_name": "admin-growth-habit-page",
    }
    return render(request, "project/admin/admin-growth-habit-page.html", context)


@login_required
def admin_growth_habit_add(request):
    context = {
        "title": "Create Growth Habit",
        "url_name": "admin-growth-habit-page",
    }
    if request.method == "POST":
        form = forms.HabitForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj: models.GrowthHabit = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Habit {obj.growth_habit} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Habit not valid.")
            context["form"] = form
    else:
        context["form"] = forms.HabitForm()

    return render(request, "project/simple-form.html", context)


@login_required
def admin_growth_habit_update(request, pk):
    obj = models.GrowthHabit.objects.get(id=pk)
    form = forms.HabitForm(instance=obj)

    if request.method == "POST":
        form = forms.HabitForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("admin-growth-habit-page")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Habit Update",
            "url_name": "admin-growth-habit-page",
        },
    )


@login_required
def admin_growth_habit_delete(request, pk):
    obj: models.GrowthHabit = models.GrowthHabit.objects.get(id=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.growth_habit)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("admin-growth-habit-page")
    context = {"object": obj, "back": "admin-growth-habit-page"}
    return render(request, "core/delete-object.html", context)
