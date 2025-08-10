from django.core.exceptions import ObjectDoesNotExist

from project.models import PlantMorphology, PlantProfile


def get_plant_by_latin_name(latin_name):
    try:
        return PlantProfile.objects.get(latin_name=latin_name)
    except ObjectDoesNotExist:
        return None


def get_morphology_aspect(element) -> PlantMorphology:
    """
    Get the morphology aspect of a plant.
    :param element: The morphology string to match.
    :return: PlantMorphology instance or None if not found.
    """
    try:
        return PlantMorphology.objects.get(element=element)
    except ObjectDoesNotExist:
        # If the morphology does not exist, create a new one.
        return PlantMorphology.objects.create(element=element)
