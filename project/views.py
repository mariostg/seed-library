from django.shortcuts import render, redirect
from project import utils, models
from project import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your views here.
def index(request):
    return render(request, "project/index.html")


@login_required
def toggle_availability(request, pk):
    plant = models.PlantProfile.objects.get(pk=pk)
    print(plant)
    plant.seed_availability = not plant.seed_availability
    plant.save()
    plant = models.PlantProfile.objects.get(pk=pk)
    context = {"pk": plant.pk, "availability": plant.seed_availability}
    print(context)
    return JsonResponse(context)
    # return render(request, "project/update-availability.html", context)


def plant_profile_page(request, pk):
    plant = utils.single_plant(pk)

    sharing_priority_highlight = {
        1: "ok",
        2: "maybe",
        3: "no",
        4: "enough",
        None: "",
    }

    context = {"plant": plant, "sharing_css_class": sharing_priority_highlight[plant.sharing_priority_id]}
    print("H:", plant.soil_humidity_max)
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
            print(form.errors)
            messages.error(request, "Plant Profile not valid.")
            context["form"] = form
    else:
        context["form"] = forms.PlantProfileForm
    return render(request, "project/plant-profile-form.html", context)


def plant_profile_update(request, pk):
    context = {
        "title": "Update Plant Profile",
        "url_name": "index",
    }
    obj = models.PlantProfile.objects.get(pk=pk)
    context["form"] = forms.PlantProfileForm(instance=obj)
    if request.method == "POST":
        form = forms.PlantProfileForm(request.POST, instance=obj)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.save()
            return redirect("plant-profile-page", pk=obj.pk)
    return render(request, "project/plant-profile-form.html", context)


def plant_profile_delete(request, pk):
    data = models.PlantProfile.objects.get(id=pk)
    if request.method == "POST":
        try:
            data.delete()
        except RestrictedError:
            messages.info(
                request, f"Plant Profile {data} ne peut-être effacée car il existe des éléments associés."
            )
        return redirect("plant-profile-page", pk=pk)
    context = {"data": data, "back": f"plant-profile-page/{pk}"}
    return render(request, "siteornitho/delete_template.html", context)


def search_plant(request):
    plants, initial = utils.search_plants(request)
    form = forms.SearchPlantForm(initial=initial)
    context = {"object_list": plants, "form": form, "initial": initial, "anchor": "search-results"}
    return render(request, "project/search-plant.html", context)


def update_availability(request):
    plants = utils.all_plants(request)
    context = {"object_list": plants}
    return render(request, "project/update-availability.html", context)


def color_table(request):
    data = models.Color.objects.all().order_by("color")
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
    data = models.Habit.objects.all().order_by("habit")
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
            messages.error(request, f"Color not valid.")
            context["form"] = form
            print("DID NOT VALIDATE")
    else:
        context["form"] = forms.ColorForm

    return render(request, "project/simple-form.html", context)


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
            messages.error(request, f"Dormancy not valid.")
            context["form"] = form
    else:
        context["form"] = forms.DormancyForm

    return render(request, "project/simple-form.html", context)


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
                messages.error(request, f"Harvesting Indicator {obj.harvesting_indicator} exists already.")
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
                messages.error(request, f"Harvesting Mean {obj.harvesting_mean} exists already.")
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


def color_update(request, pk):
    color = models.Color.objects.get(id=pk)
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


def habit_update(request, pk):
    obj = models.Habit.objects.get(id=pk)
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


def color_delete(request, pk):
    obj = models.Color.objects.get(id=pk)
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


def habit_delete(request, pk):
    obj: models.Habit = models.Habit.objects.get(id=pk)
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
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "site-admin")
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "project/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def siteadmin(request):
    return render(request, "project/admin.html")
