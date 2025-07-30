import csv
import io

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import OuterRef, RestrictedError, Subquery, Value
from django.db.models.functions import Coalesce
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from reportlab.lib.colors import black, pink, red
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from project import filters, forms, models, utils
from project.models import ProjectUser


# Create your views here.
def index(request):
    return render(request, "project/index.html")


@login_required
def toggle_availability(request, pk):
    plant = models.PlantProfile.objects.get(pk=pk)
    plant.seed_availability = not plant.seed_availability
    plant.save()
    plant = models.PlantProfile.objects.get(pk=pk)
    context = {"pk": plant.pk, "availability": plant.seed_availability}
    return JsonResponse(context)
    # return render(request, "project/update-availability.html", context)


def plant_profile_page(request, pk):
    plant: models.PlantProfile = utils.single_plant(pk)
    bloom_start = utils.MONTHS[plant.bloom_start]
    bloom_end = utils.MONTHS[plant.bloom_end]
    context = {
        "plant": plant,
        "title": plant.latin_name,
        "bloom_start": bloom_start,
        "bloom_end": bloom_end,
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
            obj: models.PlantProfile = form.save(commit=False)
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
    obj = models.PlantProfile.objects.get(pk=pk)
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
    data = models.PlantProfile.objects.get(id=pk)
    if request.method == "POST":
        try:
            data.delete()
        except RestrictedError:
            messages.info(
                request,
                f"Plant Profile {data} ne peut-être effacée car il existe des éléments associés.",
            )
        return redirect("plant-profile-page", pk=pk)
    context = {"data": data, "back": f"plant-profile-page/{pk}"}
    return render(request, "siteornitho/delete_template.html", context)


def search_plant_name(request):
    if not request.GET:
        data = models.PlantProfile.objects.none()
    else:
        data = models.PlantProfile.objects.all().order_by("latin_name")
    object_list = filters.PlantProfileFilter(request.GET, queryset=data)
    hx_include = "#full_sun,#partial_sun,#full_shade,#moisture_dry,#moisture_medium,#moisture_wet,#flowering_plant,#id-checkbox-grass,#shrub,#id_checkbox_tree,#id_checkbox_vine,#color_blue,#color_green,#color_orange,#color_pink,#color_purple,#color_red,#color_white,#color_yellow,#bird_friendly,#boulevard_garden_tolerant,#butterfly_friendly,#cedar_hedge_replacement,#container_suitable,#deer_toleranbt,#drought_tolerant,#ground_cover,#hummingbird_friendly,#rock_garden,#septic_tank_safe,#shoreline_rehab,#wetland_garden,#beginner_friendly,#germinate_easy,#juglone_tolerant,#keystones_species,#nitrogen_fixer,#acidic_soil_tolerant,#limestone_tolerant,#salt_tolerant,#sand_tolerant,#transplantation_tolerant,#grasp_candidate,#produces_burs,#rabbit_tolerant,#AB,#BC,#MB,#NB,#NL,#NS,#NT,#NU,#ON,#PE,#QC,#SK,#YT,#sliderFromBloomPeriod,#sliderToBloomPeriod,#sliderFromPlantHeight,#sliderToPlantHeight,#sliderFromPlantWidth,#sliderToPlantWidth,#sliderWinterSowingRequirements,#sliderHarvestingPeriodStart"
    context = {
        "object_list": object_list.qs,
        "url_name": "index",
        "title": "Plant Profile Filter",
        "item_count": object_list.qs.count(),
        "hx_include": hx_include,
    }
    template = (
        "project/plant-search-results.html"
        if request.htmx
        else "project/plant-catalog.html"
    )
    return render(request, template, context)


def advanced_search_plant(request):
    has_filter = False
    if not request.GET:
        data = models.PlantProfile.objects.none()
    else:
        data = models.PlantProfile.objects.all().order_by("latin_name")
        has_filter = True
    search_filter = filters.PlantProfileFilter(request.GET, queryset=data)
    object_list = search_filter.qs
    if not request.user.is_anonymous:
        object_list = object_list.annotate(
            is_owner=Coalesce(
                Subquery(
                    models.PlantCollection.objects.filter(
                        owner=request.user, plants=OuterRef("pk")
                    )
                    .annotate(owns=Value("Yes"))
                    .values("owns")
                ),
                Value("No"),
            )
        )
    return render(
        request,
        "project/plant-search-advanced.html",
        {
            "filter": search_filter,
            "object_list": object_list,
            "has_filter": has_filter,
            "url_name": "search-plant",
            "title": "Plant Profile Filter",
        },
    )


# @login_required
def update_availability(request):
    plants = utils.all_plants(request)
    context = {"object_list": plants}
    return render(request, "project/update-availability.html", context)


def color_table(request):
    data = models.BloomColor.objects.all().order_by("color")
    context = {
        "data": data,
        "url_name": "color-table",
        "title": "Colors",
    }
    return render(request, "project/color-table.html", context)


def dormancy_table(request):
    data = models.Dormancy.objects.all().order_by("dormancy")
    context = {
        "data": data,
        "url_name": "dormancy-table",
        "title": "Dormancies",
    }
    return render(request, "project/dormancy-table.html", context)


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


# @login_required
def color_add(request):
    context = {
        "title": "Create Color",
        "url_name": "color-table",
    }
    if request.method == "POST":
        form = forms.ColorForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Color {obj.color} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Color not valid.")
            context["form"] = form
    else:
        context["form"] = forms.ColorForm

    return render(request, "project/simple-form.html", context)


# @login_required
def dormancy_add(request):
    context = {
        "title": "Create Dormancy",
        "url_name": "dormancy-table",
    }
    if request.method == "POST":
        form = forms.DormancyForm(request.POST)
        if form.is_valid():
            context["form"] = form
            obj = form.save(commit=False)
            try:
                form.save()
            except IntegrityError:
                messages.error(request, f"Dormancy {obj.dormancy} exists already.")
                return render(
                    request,
                    "project/simple-form.html",
                    context,
                )
        else:
            messages.error(request, "Dormancy not valid.")
            context["form"] = form
    else:
        context["form"] = forms.DormancyForm

    return render(request, "project/simple-form.html", context)


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
def color_update(request, pk):
    color = models.BloomColor.objects.get(id=pk)
    form = forms.ColorForm(instance=color)

    if request.method == "POST":
        form = forms.ColorForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return redirect("color-table")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Color Update",
            "url_name": "color-table",
        },
    )


# @login_required
def dormancy_update(request, pk):
    obj = models.Dormancy.objects.get(id=pk)
    form = forms.DormancyForm(instance=obj)

    if request.method == "POST":
        form = forms.DormancyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("dormancy-table")

    return render(
        request,
        "project/simple-form.html",
        {
            "form": form,
            "title": "Dormancy Update",
            "url_name": "dormancy-table",
        },
    )


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
def color_delete(request, pk):
    obj = models.BloomColor.objects.get(id=pk)
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
        return redirect("color-table")
    context = {"object": obj, "back": "color-table"}
    return render(request, "core/delete-object.html", context)


# @login_required
def dormancy_delete(request, pk):
    obj = models.Dormancy.objects.get(id=pk)
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
        return redirect("dormancy-table")
    context = {"object": obj, "back": "dormancy-table"}
    return render(request, "core/delete-object.html", context)


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
    plant = models.PlantProfile.objects.get(pk=pk)
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
    return render(request, "project/admin.html")


def plant_label_pdf(request, pk):
    plant_info = utils.plant_label_info(pk)
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    c.setStrokeColor(pink)
    xw = 1.52
    xm = 0.1
    yh = 1.65
    ym = 0.1
    line_spacing = 0.155

    x = [(x_ + xm) * inch * xw for x_ in range(8)]
    y = [(y_ + ym) * inch * yh for y_ in range(6)]
    c.grid(x, y)
    c.setStrokeColor(black)
    c.setFont("Times-Roman", 10)

    def draw_plant_info(c, x, y, xm, ym, line_spacing, info):
        for idx, text in enumerate(info):
            c.drawString(x + xm * inch, y + (ym + line_spacing * idx) * inch, text)

    for i in range(7):
        for j in range(5):
            draw_plant_info(c, x[i], y[j], xm, ym, line_spacing, plant_info)

    for i in range(7):
        for j in range(5):
            for k, text in enumerate(plant_info):
                c.drawString(
                    x[i] + xm * inch, y[j] + (ym + line_spacing * k) * inch, text
                )
    c.setFillColor(red)

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


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
    plant = models.PlantProfile.objects.get(pk=pk)
    if request.method == "POST":
        plant.full_sun = request.POST.get("full_sun") == "on"
        plant.partial_sun = request.POST.get("partial_sun") == "on"
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


def plant_identification_information_update(request, pk):
    plant = models.PlantProfile.objects.get(pk=pk)
    if request.method == "POST":
        plant.latin_name = request.POST.get("latin_name")
        plant.english_name = request.POST.get("english_name")
        plant.french_name = request.POST.get("french_name")
        plant.taxon = request.POST.get("taxon")
        plant.inaturalist_taxon = request.POST.get("inaturalist_taxon")
        plant.save()
        messages.success(request, "Identification information updated successfully.")
        return redirect("plant-profile-page", pk=plant.pk)

    context = {
        "title": f"{plant.latin_name} - Identification Information",
        "plant": plant,
    }
    return render(
        request, "project/plant-identification-information-update.html", context
    )


def plant_growth_characteristics_update(request, pk):
    plant = models.PlantProfile.objects.get(pk=pk)
    growth_habits = models.GrowthHabit.objects.all().order_by("growth_habit")
    lifespan_choices = models.PlantLifespan.objects.all().order_by("lifespan")
    bloom_colors = models.BloomColor.objects.all().order_by("bloom_color")
    bloom_starts = bloom_ends = utils.MONTHS
    if request.method == "POST":
        plant.max_height = request.POST.get("max_height")
        plant.max_width = request.POST.get("max_width")
        plant.growth_habit = models.GrowthHabit.objects.get(
            pk=request.POST.get("growth_habit")
        )
        plant.does_not_spread = request.POST.get("does_not_spread") == "on"
        plant.lifespan = models.PlantLifespan.objects.get(
            pk=request.POST.get("lifespan")
        )
        plant.dioecious = request.POST.get("dioecious") == "on"
        plant.bloom_start = request.POST.get("bloom_start")
        plant.bloom_end = request.POST.get("bloom_end")
        plant.bloom_color = models.BloomColor.objects.get(
            pk=request.POST.get("bloom_color")
        )
        plant.save()
        messages.success(request, "Growth characteristics updated successfully.")
        return redirect("plant-profile-page", pk=plant.pk)

    context = {
        "title": f"{plant.latin_name} - Growth Characteristics",
        "plant": plant,
        "growth_habits": growth_habits,
        "bloom_colors": bloom_colors,
        "bloom_starts": bloom_starts,
        "bloom_ends": bloom_ends,
        "lifespan_choices": lifespan_choices,
    }
    return render(request, "project/plant-growth-characteristics-update.html", context)


def plant_propagation_and_cultivation_update(request, pk):
    plant = models.PlantProfile.objects.get(pk=pk)

    # packaging measures
    packaging_measures = models.PackagingMeasure.objects.all().order_by(
        "packaging_measure"
    )
    if not packaging_measures:
        messages.warning(
            request, "No packaging measures available. Please add some first."
        )
        return redirect("packaging-measure-table")

    # One Cultivars
    one_cultivars = models.OneCultivar.objects.all().order_by("one_cultivar")
    if not one_cultivars:
        messages.warning(request, "No one cultivars available. Please add some first.")
        return redirect("one-cultivar-table")

    # Seed Viability Tests
    seed_viability_tests = models.SeedViabilityTest.objects.all().order_by(
        "seed_viability_test"
    )
    if not seed_viability_tests:
        messages.warning(
            request, "No seed viability tests available. Please add some first."
        )
        return redirect("seed-viability-test-table")

    # Seed Storage
    seed_storage = models.SeedStorage.objects.all().order_by("seed_storage")
    if not seed_storage:
        messages.warning(
            request, "No seed storage options available. Please add some first."
        )
        return redirect("seed-storage-table")

    # seed preparation
    seed_preparation = models.SeedPreparation.objects.all().order_by("seed_preparation")
    if not seed_preparation:
        messages.warning(
            request, "No seed preparation available. Please add some first."
        )
        return redirect("seed-preparation-table")

    # sowing depth
    sowing_depth = models.SowingDepth.objects.all().order_by("sowing_depth")
    if not sowing_depth:
        messages.warning(request, "No sowing depth available. Please add some first.")
        return redirect("sowing-depth-table")

    if request.method == "POST":
        # seed handling related fields
        plant.seed_availability = request.POST.get("seed_availability") == "on"
        plant.accepting_seed = request.POST.get("accepting_seed") == "on"

        viability_test_id = request.POST.get("viability_test")
        if viability_test_id:
            try:
                plant.seed_viability_test = models.SeedViabilityTest.objects.get(
                    pk=viability_test_id
                )
            except models.SeedViabilityTest.DoesNotExist:
                messages.warning(request, "Selected seed viability test not found.")
        else:
            plant.seed_viability_test = None
        plant.seed_storage = request.POST.get("seed_storage")

        one_cultivar_id = request.POST.get("one_cultivar")
        if one_cultivar_id:
            try:
                plant.one_cultivar = models.OneCultivar.objects.get(pk=one_cultivar_id)
            except models.OneCultivar.DoesNotExist:
                messages.warning(request, "Selected one cultivar not found.")
        else:
            plant.one_cultivar = None

        packaging_measure_id = request.POST.get("packaging_measure")
        if packaging_measure_id:
            try:
                plant.packaging_measure = models.PackagingMeasure.objects.get(
                    pk=packaging_measure_id
                )
            except models.PackagingMeasure.DoesNotExist:
                messages.warning(request, "Selected packaging measure not found.")
        else:
            plant.packaging_measure = None

        dormancy_id = request.POST.get("dormancy")
        if dormancy_id:
            try:
                plant.dormancy = models.Dormancy.objects.get(pk=dormancy_id)
            except models.Dormancy.DoesNotExist:
                messages.warning(request, "Selected dormancy not found.")
        else:
            plant.dormancy = None

        seed_preparation_id = request.POST.get("seed_preparation")
        if seed_preparation_id:
            try:
                plant.seed_preparation = models.SeedPreparation.objects.get(
                    pk=seed_preparation_id
                )
            except models.SeedPreparation.DoesNotExist:
                messages.warning(request, "Selected seed preparation not found.")
        else:
            plant.seed_preparation = None

        plant.seed_cleaning_notes = request.POST.get("seed_cleaning_notes")

        seed_storage_label_info_id = request.POST.get("seed_storage_label_info")
        if seed_storage_label_info_id:
            try:
                plant.seed_storage_label_info = models.SeedStorageLabelInfo.objects.get(
                    pk=seed_storage_label_info_id
                )
            except models.SeedStorageLabelInfo.DoesNotExist:
                messages.warning(request, "Selected seed storage label info not found.")
        else:
            plant.seed_storage_label_info = None

        plant.save()
        messages.success(request, "Propagation and cultivation updated successfully.")
        return redirect("plant-profile-page", pk=plant.pk)

    context = {
        "title": f"{plant.latin_name} - Propagation and Cultivation",
        "plant": plant,
        "packaging_measures": packaging_measures,
        "one_cultivars": one_cultivars,
        "seed_viability_tests": seed_viability_tests,
        "seed_storage": seed_storage,
        "seed_preparation": seed_preparation,
        "sowing_depth": sowing_depth,
    }
    return render(
        request, "project/plant-propagation-and-cultivation-update.html", context
    )
