import django_filters

from project import models, utils


class PlantProfileFilter(django_filters.FilterSet):
    """Filters used on plant profile search form"""

    latin_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    english_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    french_name = django_filters.CharFilter(
        method="filter_icontains",
    )
    light_from = django_filters.ModelChoiceFilter(
        queryset=models.Lighting.objects.all(),
        method="filter_gte",
    )
    light_to = django_filters.ModelChoiceFilter(
        queryset=models.Lighting.objects.all(),
        method="filter_lte",
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
    harvesting_end = django_filters.ChoiceFilter(
        choices=utils.MONTHS,
        method="filter_lte",
    )
    germinate_easy = django_filters.BooleanFilter(
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
    seed_availability = django_filters.BooleanFilter(
        method="filter_bool",
    )

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
        return queryset.filter(**{"germinate_easy": value})

    class Meta:
        model = models.PlantProfile
        fields = ["latin_name", "bloom_start", "bloom_end"]
