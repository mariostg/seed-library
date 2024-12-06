from django.shortcuts import render
from project import utils, models
from project import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
