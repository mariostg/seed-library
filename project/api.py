# This api uses the djang-ninja framework to create a RESTful API for the plant profiles.

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router
from ninja.security import APIKeyHeader

from project.models import PlantProfile

router = Router()


# define a get decorator to the root url
# define a method named home that take a request as an argument and return a string
@router.get("/")
def home(request):
    return "Hello, world!"


@router.get("/version/")
def version(request):
    data = {
        "version": "1.0.0",
    }
    return data


class APIKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == "test":
            return key

        return None


api_key = APIKey()


# Define a class named PlantProfileSchema that inherits from ModelSchema
# The PlantProfileSchema class is used to serialize the PlantProfile model
class PlantProfileSchema(ModelSchema):
    sharing_priority: str

    class Meta:
        model = PlantProfile
        fields = [
            "id",
            "latin_name",
            "english_name",
            "french_name",
            "bloom_start",
            "bloom_end",
            "harvesting_start",
            "germinate_easy",
            "max_height",
            "stratification_duration",
            "seed_availability",
        ]

    # define a static method named get_sharing_priority that takes a plant_profile as an argument and return the sharing_priority level
    @staticmethod
    def resolve_sharing_priority_level(plant_profile):
        return plant_profile.sharing_priority.level

    @staticmethod
    def resolve_sharing_priority(plant_profile):
        return plant_profile.sharing_priority.sharing_priority


# Define a get decorator to the /plant-profiles/ url
# Define a method named plant_profiles that take a request as an argument and return a list of PlantProfile objects
@router.get("/plant-profiles/", response=list[PlantProfileSchema])
def plant_profiles(request):

    return PlantProfile.objects.filter(seed_availability=True)


@router.get("/seeds-available/", response=list[PlantProfileSchema], auth=api_key)
def seeds_available(request):
    """Usage example:
    curl -X 'GET' \
    'http://127.0.0.1:8000/api/v1/seeds-available/' \
    -H 'accept: application/json' \
    -H 'X-API-Key: test'
    """
    return PlantProfile.objects.filter(seed_availability=True)


@router.get("/plant-profile/{pk}/", response=PlantProfileSchema)
def plant_profile(request, pk: int):
    """Usage exmple:
    curl -X 'GET' \
    'http://127.0.0.1:8000/api/v1/plant-profiles/' \
    -H 'accept: application/json'
    """
    return get_object_or_404(PlantProfile, pk=pk)
