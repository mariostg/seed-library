from unicodedata import normalize

import django_filters
from django.db.models import Q

from project import models, utils


class PlantProfileFilter(django_filters.FilterSet):
    """Filters used on plant profile search form"""

    any_plant_name = django_filters.CharFilter(
        method="filter_normalized_plant_name",
        strip=False,
    )

    seed_availability = django_filters.CharFilter(
        method="filter_seed_availability",
    )

    accepting_seed = django_filters.CharFilter(
        method="filter_accepting_seed",
    )
    native_to_ottawa_region = django_filters.CharFilter(
        method="filter_boolean",
    )
    beginner_friendly = django_filters.CharFilter(
        method="filter_boolean",
    )
    bird_friendly = django_filters.CharFilter(
        method="filter_boolean",
    )
    pollinator_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    butterfly_host = django_filters.CharFilter(
        method="filter_boolean",
    )
    bee_host = django_filters.CharFilter(
        method="filter_boolean",
    )
    boulevard_garden_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    hedge = django_filters.CharFilter(
        method="filter_boolean",
    )
    container_suitable = django_filters.CharFilter(
        method="filter_boolean",
    )
    drought_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    germinate_easy = django_filters.CharFilter(
        method="filter_boolean",
    )
    starter_pack = django_filters.CharFilter(
        method="filter_starter_pack",
    )

    ground_cover = django_filters.CharFilter(
        method="filter_boolean",
    )
    rock_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    rain_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    school_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    woodland_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    row_garden = django_filters.CharFilter(
        method="filter_row_garden",
    )
    does_not_spread = django_filters.CharFilter(
        method="filter_boolean",
    )
    annual = django_filters.CharFilter(
        method="filter_lifespan",
    )
    biennial = django_filters.CharFilter(
        method="filter_lifespan",
    )
    perennial = django_filters.CharFilter(
        method="filter_lifespan",
    )
    spring_ephemeral = django_filters.CharFilter(
        method="filter_boolean",
    )
    self_seeding = django_filters.CharFilter(
        method="filter_boolean",
    )
    septic_tank_safe = django_filters.CharFilter(
        method="filter_boolean",
    )
    wetland_garden = django_filters.CharFilter(
        method="filter_boolean",
    )
    grasp_candidate = django_filters.CharFilter(
        method="filter_boolean",
    )
    color_blue = django_filters.CharFilter(
        method="filter_color",
    )
    color_green = django_filters.CharFilter(
        method="filter_color",
    )
    color_orange = django_filters.CharFilter(
        method="filter_color",
    )
    color_pink = django_filters.CharFilter(
        method="filter_color",
    )
    color_purple = django_filters.CharFilter(
        method="filter_color",
    )
    color_red = django_filters.CharFilter(
        method="filter_color",
    )
    color_white = django_filters.CharFilter(
        method="filter_color",
    )
    color_yellow = django_filters.CharFilter(
        method="filter_color",
    )
    growth_habit = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    flowering_plant = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    grass = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    shrub = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    deciduous_tree = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    conifer_tree = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    vine = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    hummingbird_friendly = django_filters.CharFilter(
        method="filter_boolean",
    )
    rabbit_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    deer_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    acidic_soil_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    juglone_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    keystones_species = django_filters.CharFilter(
        method="filter_boolean",
    )
    limestone_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    nitrogen_fixer = django_filters.CharFilter(
        method="filter_boolean",
    )
    produces_burs = django_filters.CharFilter(
        method="filter_excludes",
    )
    foot_traffic_tolerance_medium = django_filters.CharFilter(
        method="filter_boolean",
    )
    salt_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    sand_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    shoreline_rehab = django_filters.CharFilter(
        method="filter_boolean",
    )
    transplantation_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    latin_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    english_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    french_name = django_filters.CharFilter(
        method="filter_icontains",
    )

    bloom_start = django_filters.ChoiceFilter(
        choices=utils.MONTHS,
        method="filter_gte",
    )
    bloom_end = django_filters.ChoiceFilter(
        choices=utils.MONTHS,
        method="filter_lte",
    )
    harvesting_start = django_filters.ChoiceFilter(
        choices=utils.MONTHS,
        method="filter_gte",
    )

    max_height = django_filters.NumberFilter(
        method="filter_lte",
    )
    max_width = django_filters.NumberFilter(
        method="filter_lte",
    )
    stratification_duration = django_filters.NumberFilter(
        method="filter_lte",
    )

    full_sun = django_filters.CharFilter(
        method="filter_boolean",
    )
    part_shade = django_filters.CharFilter(
        method="filter_boolean",
    )
    full_shade = django_filters.CharFilter(
        method="filter_boolean",
    )

    moisture_dry = django_filters.CharFilter(
        method="filter_boolean",
    )
    moisture_medium = django_filters.CharFilter(
        method="filter_boolean",
    )
    moisture_wet = django_filters.CharFilter(
        method="filter_boolean",
    )

    cause_skin_rashes = django_filters.CharFilter(
        method="filter_excludes",
    )

    # Admin Filters
    is_draft = django_filters.CharFilter(
        method="filter_boolean",
    )
    is_active = django_filters.CharFilter(
        method="filter_excludes",
    )
    is_accepted = django_filters.CharFilter(
        method="filter_excludes",
    )

    def filter_normalized_plant_name(self, queryset, name, value):
        normalized_value = (
            normalize("NFKD", value).encode("ASCII", "ignore").decode("ASCII").lower()
        )

        # Get all plant profiles
        all_plants = queryset.all()
        matching_ids = []

        # Filter manually to handle accents in all name fields
        for plant in all_plants:
            # Check french_name
            if plant.french_name:
                normalized_name = (
                    normalize("NFKD", plant.french_name)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .lower()
                )
                if normalized_value in normalized_name:
                    matching_ids.append(plant.id)
                    continue

            # Check latin_name
            if plant.latin_name:
                normalized_name = (
                    normalize("NFKD", plant.latin_name)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .lower()
                )
                if normalized_value in normalized_name:
                    matching_ids.append(plant.id)
                    continue

            # Check english_name
            if plant.english_name:
                normalized_name = (
                    normalize("NFKD", plant.english_name)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                    .lower()
                )
                if normalized_value in normalized_name:
                    matching_ids.append(plant.id)
                    continue

        return queryset.filter(id__in=matching_ids)

    def filter_any_name(self, queryset, name, value):
        return queryset.filter(
            Q(**{"latin_name__icontains": value})
            | Q(**{"english_name__icontains": value})
            | Q(**{"french_name__icontains": value})
        )

    def filter_growth_habit(self, queryset, name, value):
        if value:
            return queryset.filter(growth_habit__growth_habit=value)

        else:
            return queryset.none()

    def filter_starter_pack(self, queryset, name, value):
        if value == "starter_pack_shade":
            return queryset.filter(starter_pack_shade=True)
        elif value == "starter_pack_sun_dry":
            return queryset.filter(starter_pack_sun_dry=True)
        elif value == "starter_pack_sun_wet":
            return queryset.filter(starter_pack_sun_wet=True)
        else:
            return queryset.none()

    def filter_color(self, queryset, name, value):
        if value:
            return queryset.filter(bloom_color__bloom_color=value)
        else:
            return queryset.none()

    def filter_lifespan(self, queryset, name, value):
        if value:
            return queryset.filter(lifespan__lifespan=value)
        else:
            return queryset.none()

    def filter_seed_availability(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: True})
        else:
            return queryset.exclude(**{name: True})

    def filter_accepting_seed(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: True})
        else:
            return queryset.exclude(**{name: True})

    def filter_icontains(self, queryset, name, value):
        lookup = "__".join([name, "icontains"])
        return queryset.filter(**{lookup: value})

    def filter_lte(self, queryset, name, value):
        lookup = "__".join([name, "lte"])
        d = queryset.filter(**{lookup: value})
        return d

    def filter_gte(self, queryset, name, value):
        lookup = "__".join([name, "gte"])
        return queryset.filter(**{lookup: value})

    def filter_latin_name(self, queryset, name, value):
        return queryset.filter(**{"latin_name": value})

    def filter_boolean(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: True})
        else:
            return queryset.exclude(**{name: True})

    def filter_excludes(self, queryset, name, value):
        return queryset.filter(**{name: False})

    def filter_row_garden(self, queryset, name, value):
        # filter for plants that have a max height of 2 feet or less
        return queryset.filter(max_height__lte=2)

    class Meta:
        model = models.PlantProfile
        fields = ["latin_name", "bloom_start", "bloom_end", "seed_availability"]
