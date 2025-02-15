from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from project import models

# class HarvestingPeriodFilter(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = "Harvesting Period"

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = "period"

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return [
#             ("7", "july"),
#             ("8", "aug"),
#         ]

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         return queryset.filter(
#             harvest_start__gte=6,
#             harvest_end__lte=8,
#         )


class PlantProfileAdmin(admin.ModelAdmin):
    # list_filter = ["harvest_start",]
    search_fields = ["latin_name", "french_name"]


admin.site.register(models.PlantProfile, PlantProfileAdmin)
admin.site.register(models.SharingPriority)
admin.site.register(models.HarvestingIndicator)
admin.site.register(models.HarvestingMean)
admin.site.register(models.SeedHead)
admin.site.register(models.ViablityTest)
admin.site.register(models.SeedStorage)
admin.site.register(models.OneCultivar)
admin.site.register(models.PackagingMeasure)
admin.site.register(models.Dormancy)
admin.site.register(models.SeedPreparation)
admin.site.register(models.SeedStorageLabelInfo)
admin.site.register(models.Lighting)
admin.site.register(models.SoilHumidity)
admin.site.register(models.Color)
admin.site.register(models.Habit)
admin.site.register(models.SowingDepth)
admin.site.register(models.ProjectUser, UserAdmin)
admin.site.register(models.PlantCollection)
admin.site.register(models.PlantImage)
admin.site.register(models.PlantMorphology)
