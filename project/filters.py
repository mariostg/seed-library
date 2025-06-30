import django_filters
from django.db.models import Q

from project import models, utils


class PlantProfileFilter(django_filters.FilterSet):
    """Filters used on plant profile search form"""

    any_name = django_filters.CharFilter(
        method="filter_any_name",
    )

    seed_availability = django_filters.CharFilter(
        method="filter_seed_availability",
    )

    accepting_seed = django_filters.CharFilter(
        method="filter_accepting_seed",
    )

    bird_friendly = django_filters.CharFilter(
        method="filter_boolean",
    )
    butterfly_friendly = django_filters.CharFilter(
        method="filter_boolean",
    )
    boulevard_garden_tolerant = django_filters.CharFilter(
        method="filter_boolean",
    )
    cedar_hedge_replacement = django_filters.CharFilter(
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
    ground_cover = django_filters.CharFilter(
        method="filter_boolean",
    )
    rock_garden = django_filters.CharFilter(
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
    tree = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    vine = django_filters.CharFilter(
        method="filter_growth_habit",
    )
    hummingbird_friendly = django_filters.CharFilter(
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
    stratification_duration = django_filters.NumberFilter(
        method="filter_lte",
    )
    sharing_priority = django_filters.ModelChoiceFilter(
        queryset=models.SharingPriority.objects.all(),
    )

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

    def filter_color(self, queryset, name, value):
        if value:
            return queryset.filter(bloom_color__bloom_color=value)
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
        return queryset.filter(**{lookup: value})

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

    class Meta:
        model = models.PlantProfile
        fields = ["latin_name", "bloom_start", "bloom_end", "seed_availability"]
