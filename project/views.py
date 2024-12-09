from django.shortcuts import render, redirect
from project import utils, models
from project import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request, "project/index.html")


@login_required
def toggle_availability(request, pk):
    plant = models.SeedLibrary.objects.get(pk=pk)
    print(plant)
    plant.seed_availability = not plant.seed_availability
    plant.save()
    plant = models.SeedLibrary.objects.get(pk=pk)
    context = {"pk": plant.pk, "availability": plant.seed_availability}
    print(context)
    return JsonResponse(context)
    # return render(request, "project/update-availability.html", context)


def search_plant(request):
    plants, initial = utils.search_plants(request)
    form = forms.SearchPlantForm(initial=initial)
    context = {"object_list": plants, "form": form, "initial": initial, "anchor": "search-results"}
    return render(request, "project/search-plant.html", context)


def update_availability(request):
    plants = utils.all_plants(request)
    context = {"object_list": plants}
    return render(request, "project/update-availability.html", context)


def single_plant(request, pk):
    plant = utils.single_plant(pk)
    sharing_priority_highlight = {1: "ok", 2: "maybe", 3: "no", 4: "enough"}

    context = {"plant": plant, "sharing_css_class": sharing_priority_highlight[plant.sharing_priority_id]}
    print("H:", plant.soil_humidity_max)
    return render(request, "project/single-plant.html", context)


def color_table(request):
    data = models.Color.objects.all().order_by("color")
    context = {
        "data": data,
        "url_name": "color-table",
        "title": "Colors",
    }
    return render(request, "project/color-table.html", context)


def habit_table(request):
    data = models.Habit.objects.all().order_by("habit")
    context = {
        "data": data,
        "url_name": "habit-table",
        "title": "Habits",
    }
    return render(request, "project/habit-table.html", context)


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


def color_delete(request, pk):
    color = models.Color.objects.get(id=pk)
    if request.method == "POST":
        try:
            color.delete()
        except RestrictedError as e:
            msg = e.args[0].split(":")[0] + " : "
            fkeys = []
            for fk in e.restricted_objects:
                fkeys.append(fk.color)
            msg = msg + ", ".join(fkeys)
            messages.warning(request, msg)
        return redirect("color-table")
    context = {"object": color, "back": "color-table"}
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
