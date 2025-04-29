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

    latin_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    english_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    french_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    soil_humidity_min = django_filters.ModelChoiceFilter(
        queryset=models.SoilHumidity.objects.all(),
        method="filter_gte",
    )
    soil_humidity_max = django_filters.ModelChoiceFilter(
        queryset=models.SoilHumidity.objects.all(),
        method="filter_lte",
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
    germinate_easy = django_filters.BooleanFilter(
        field_name="germinate_easy",
        method="filter_bool",
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

    def filter_bool(self, queryset, name, value):
        return queryset.filter(**{name: value})

    class Meta:
        model = models.PlantProfile
        fields = ["latin_name", "bloom_start", "bloom_end", "seed_availability"]
