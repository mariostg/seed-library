from PIL import Image, ImageOps
from django.db import models
from django.utils.dates import MONTHS
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        ordering = ["harvesting_indicator"]


class HarvestingMean(Base):
    harvesting_mean = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.harvesting_mean

    class Meta:
        ordering = ["harvesting_mean"]


class SeedHead(Base):
    seed_head = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.seed_head

    class Meta:
        ordering = ["seed_head"]


class ViablityTest(Base):
    viability_test = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.viability_test

    class Meta:
        ordering = ["viability_test"]


class SeedStorage(Base):
    seed_storage = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.seed_storage


class OneCultivar(Base):
    one_cultivar = models.CharField(max_length=125, blank=True)

    def __str__(self) -> str:
        return self.one_cultivar

    class Meta:
        ordering = ["one_cultivar"]


class PackagingMeasure(Base):
    packaging_measure = models.CharField(max_length=35, blank=True)

    def __str__(self) -> str:
        return self.packaging_measure

    class Meta:
        ordering = ["packaging_measure"]


class Dormancy(Base):
    dormancy = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.dormancy


class SeedPreparation(Base):
    seed_preparation = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.seed_preparation

    class Meta:
        ordering = ["seed_preparation"]


class SeedStorageLabelInfo(Base):
    seed_storage_label_info = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.seed_storage_label_info

    class Meta:
        ordering = ["seed_storage_label_info"]


class SowingDepth(Base):
    sowing_depth = models.CharField(max_length=25, blank=True)

    def __str__(self) -> str:
        return self.sowing_depth

    class Meta:
        ordering = ["sowing_depth"]


class Lighting(Base):
    lighting = models.CharField(unique=True, max_length=45, blank=True)
    definition = models.CharField(max_length=75, blank=True)

    def __str__(self) -> str:
        return f"{self.lighting} - {self.definition}"


class Color(Base):
    color = models.CharField(unique=True, max_length=25, blank=True)

    def __str__(self) -> str:
        return self.color

    def save(self, *args, **kwargs):
        self.color = self.color.capitalize()
        super(Color, self).save(*args, **kwargs)


class Habit(Base):
    habit = models.CharField(unique=True, max_length=30, blank=True)

    def __str__(self) -> str:
        return self.habit

    class Meta:
        ordering = ["habit"]


class SoilHumidity(Base):
    soil_humidity = models.CharField(max_length=45, blank=True)
    definition = models.CharField(max_length=75, blank=True)

    def __str__(self) -> str:
        return f"{self.soil_humidity} - {self.definition}"


class PlantProfile(Base):
    latin_name = models.CharField(max_length=75, unique=True)
    english_name = models.CharField(max_length=75, blank=True)
    french_name = models.CharField(max_length=75, blank=True)
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
    min_height = models.SmallIntegerField(blank=True, null=True, default=0)
    max_height = models.SmallIntegerField(blank=True, null=True, default=0)
    size = models.CharField(max_length=35, blank=True)
    stratification_detail = models.CharField(max_length=55, blank=True)
    stratification_duration = models.SmallIntegerField(blank=True, null=True, default=0)
    sowing_depth = models.ForeignKey(SowingDepth, on_delete=models.RESTRICT, blank=True, null=True)
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
    keystones_species = models.BooleanField(default=False, null=True, blank=True)
    draught_tolerent = models.BooleanField(default=False, null=True, blank=True)
    salt_tolerent = models.BooleanField(default=False, null=True, blank=True)
    deer_tolerent = models.BooleanField(default=False, null=True, blank=True)
    easy_to_contain = models.BooleanField(default=False, null=True, blank=True)
    flower_color = models.ForeignKey(Color, on_delete=models.RESTRICT, null=True, blank=True)
    habit = models.ForeignKey(Habit, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.latin_name} | {self.english_name} | {self.french_name}| {self.soil_humidity_max}"

    class Meta:
        ordering = ["latin_name"]

    def compare_heights(self):
        if self.min_height and self.max_height and self.min_height > self.max_height:
            raise ValidationError(
                f"{self.latin_name}: Minimum height ({self.min_height}) must be smaller than maximum height ({self.max_height})"
            )

    def compare_blooming(self):
        if not self.bloom_start:
            self.bloom_start = 0
        if not self.bloom_end:
            self.bloom_end = 0
            self.bloom_start = 0
        if self.bloom_start and self.bloom_end and self.bloom_start > self.bloom_end:
            raise ValidationError("Beginning of blooming period must be before end of blooming period")

    def save(self, *args, **kwargs):
        if not self.harvesting_start:
            self.harvesting_start = 0
        if not self.harvesting_end:
            self.harvesting_end = 0
        if not self.latin_name:
            raise ValueError("Missing Latin Name")
        self.compare_heights()
        self.compare_blooming()
        super(PlantProfile, self).save(*args, **kwargs)


class ProjectUser(AbstractUser):
    plants = models.ManyToManyField(PlantProfile, through="PlantCollection")

    def __str__(self):
        return str(self.username)


class PlantCollection(models.Model):
    owner = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    plants = models.ForeignKey(PlantProfile, on_delete=models.CASCADE)
    details = models.CharField(max_length=125, blank=True)

    def __str__(self):
        return f"{self.owner}, {self.plants}"

    class Meta:
        ordering = ["plants__latin_name"]
        constraints = [
            models.UniqueConstraint(name="unique_plant_owner", fields=["owner", "plants"]),
        ]


class PlantMorphology(models.Model):
    """Morphological elements of a plant such as leaf, fruit, flower, stem, etc."""

    element = models.CharField(max_length=75, blank=True, unique=True)

    def __str__(self):
        return self.element

    class Meta:
        ordering = ["element"]
        verbose_name_plural = "plant morphology"


class PlantImage(models.Model):
    plant_profile = models.ForeignKey(PlantProfile, on_delete=models.CASCADE, related_name="images")
    morphology_aspect = models.ForeignKey(PlantMorphology, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Titre", max_length=125)
    description = models.CharField(verbose_name="Description", max_length=55, blank=True)
    photo_author = models.CharField(verbose_name="Auteur", max_length=125)
    photo_date = models.DateField(verbose_name="Date photo")
    image = models.ImageField(upload_to="project/images")

    def __str__(self) -> str:
        return f"{self.plant_profile.latin_name} - {self.title} - {self.photo_author}"

    def save(self, *args, **kwargs):
        try:  # Delete plant if it exists
            this = PlantImage.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
        img = Image.open(self.image)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        target_width = 1024
        h_coefficient = width / 1024
        target_height = height / h_coefficient
        img = img.resize((int(target_width), int(target_height)), Image.LANCZOS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()

    def get_size(self):
        try:
            img = PIL.Image.open(self.image)
        except FileNotFoundError:
            return 0
        width, height = img.size
        img.close()
        size = {"width": width, "height": height}
        return size

    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except ValueError:
            pass
        super(PlantImage, self).delete(*args, **kwargs)
