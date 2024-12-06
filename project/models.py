from django.db import models
from django.utils.dates import MONTHS


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SharingPriority(Base):
    sharing_priority = models.CharField(max_length=75, blank=True)

    def __str__(self) -> str:
        return self.sharing_priority


class HarvestingIndicator(Base):
    harvesting_indicator = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.harvesting_indicator


class HarvestingMean(Base):
    harvesting_mean = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.harvesting_mean


class SeedHead(Base):
    seed_head = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.seed_head


class ViablityTest(Base):
    viability_test = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.viability_test


class SeedStorage(Base):
    seed_storage = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.seed_storage


class OneCultivar(Base):
    one_cultivar = models.CharField(max_length=125, blank=True)

    def __str__(self) -> str:
        return self.one_cultivar


class PackagingMeasure(Base):
    packaging_measure = models.CharField(max_length=35, blank=True)

    def __str__(self) -> str:
        return self.packaging_measure


class Dormancy(Base):
    dormancy = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.dormancy


class SeedPreparation(Base):
    seed_preparation = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.seed_preparation


class SeedStorageLabelInfo(Base):
    seed_storage_label_info = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.seed_storage_label_info


class Lighting(Base):
    lighting = models.CharField(max_length=45, blank=True)

    def __str__(self) -> str:
        return self.lighting


class SoilHumidity(Base):
    soil_humidity = models.CharField(max_length=45, blank=True)

    def __str__(self) -> str:
        return self.soil_humidity


class SeedLibrary(Base):
    latin_name = models.CharField(max_length=75)
    english_name = models.CharField(max_length=75)
    french_name = models.CharField(max_length=75)
    url = models.CharField(max_length=250, blank=True)
    light_from = models.ForeignKey(
        Lighting, related_name="light_from", on_delete=models.RESTRICT, blank=True, null=True
    )
    light_to = models.ForeignKey(
        Lighting, related_name="light_to", on_delete=models.RESTRICT, blank=True, null=True
    )
    bloom_start = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    bloom_end = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    soil_humidity_min = models.ForeignKey(
        SoilHumidity, related_name="soil_humidity_min", on_delete=models.RESTRICT, blank=True, null=True
    )
    soil_humidity_max = models.ForeignKey(
        SoilHumidity, related_name="soil_humidity_max", on_delete=models.RESTRICT, blank=True, null=True
    )
    min_height = models.SmallIntegerField(blank=True, default=0)
    max_height = models.SmallIntegerField(blank=True, default=0)
    size = models.CharField(max_length=35, blank=True)
    stratification_detail = models.CharField(max_length=55, blank=True)
    stratification_duration = models.SmallIntegerField(blank=True, default=0)
    sowing_depth = models.CharField(max_length=55, blank=True)
    sowing_period = models.CharField(max_length=55, blank=True)
    sharing_priority = models.ForeignKey(SharingPriority, on_delete=models.RESTRICT, blank=True, null=True)
    harvesting_start = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    harvesting_end = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    harvesting_indicator = models.ForeignKey(
        HarvestingIndicator, on_delete=models.RESTRICT, null=True, blank=True
    )
    harvesting_mean = models.ForeignKey(HarvestingMean, on_delete=models.RESTRICT, null=True, blank=True)
    seed_head = models.ForeignKey(SeedHead, on_delete=models.RESTRICT, null=True, blank=True)
    remove_non_seed_material = models.BooleanField(default=False, null=True, blank=True)
    viability_test = models.ForeignKey(ViablityTest, on_delete=models.RESTRICT, null=True, blank=True)
    seed_storage = models.ForeignKey(SeedStorage, on_delete=models.RESTRICT, null=True, blank=True)
    one_cultivar = models.ForeignKey(OneCultivar, on_delete=models.RESTRICT, null=True, blank=True)
    packaging_measure = models.ForeignKey(PackagingMeasure, on_delete=models.RESTRICT, null=True, blank=True)
    dormancy = models.ForeignKey(Dormancy, on_delete=models.RESTRICT, null=True, blank=True)
    seed_preparation = models.ForeignKey(SeedPreparation, on_delete=models.RESTRICT, null=True, blank=True)
    hyperlink = models.CharField(max_length=200, blank=True)
    envelope_label_link = models.CharField(max_length=200, blank=True)
    harvesting_video_link = models.CharField(max_length=200, blank=True)
    seed_picture_link = models.CharField(max_length=200, blank=True)
    pods_seed_head_picture_link = models.CharField(max_length=200, blank=True)
    seed_storage_label_info = models.ForeignKey(
        SeedStorageLabelInfo, on_delete=models.RESTRICT, null=True, blank=True
    )
    notes = models.CharField(max_length=450, blank=True)
    germinate_easy = models.BooleanField(default=False, null=True, blank=True)
    rock_garden = models.BooleanField(default=False, null=True, blank=True)
    rain_garden = models.BooleanField(default=False, null=True, blank=True)
    pond_edge = models.BooleanField(default=False, null=True, blank=True)
    shoreline_rehab = models.BooleanField(default=False, null=True, blank=True)
    container_suitable = models.BooleanField(default=False, null=True, blank=True)
    ground_cover = models.BooleanField(default=False, null=True, blank=True)
    garden_edge = models.BooleanField(default=False, null=True, blank=True)
    woodland_garden = models.BooleanField(default=False, null=True, blank=True)
    wind_break_hedge = models.BooleanField(default=False, null=True, blank=True)
    erosion_control = models.BooleanField(default=False, null=True, blank=True)
    seed_availability = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.latin_name} | {self.english_name} | {self.french_name}| {self.soil_humidity_max}"
