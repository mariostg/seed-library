from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.dates import MONTHS
from PIL import Image, ImageOps


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SharingPriority(Base):
    """
    A model class representing sharing priority levels for the seeds.

    This class defines different levels of sharing priority that can be assigned
    to Seed Profile, ranging from none to high priority.

    Attributes:
        LEVELS (dict): Dictionary mapping priority level keys to their display names.
            Available levels are: none, low, medium, and high.
        sharing_priority (CharField): A field to store custom sharing priority text (max 75 chars).
        level (CharField): The actual priority level, chosen from LEVELS dictionary.
            Defaults to "None" if not specified.

    Example:
        >>> priority = SharingPriority(sharing_priority="1 Give in Priority", level="high")
        >>> str(priority)
        '1 Give in Priority'
    """

    LEVELS = {
        "none": "None",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }
    sharing_priority = models.CharField(max_length=75, blank=True)
    level = models.CharField(choices=LEVELS, blank=True, default="None", max_length=10)

    def __str__(self) -> str:
        return self.sharing_priority


class HarvestingIndicator(Base):
    """
    Model representing a Harvesting Indicator. This indicator provides a clue as to when the seeds are ready for harvesting.

    Attributes:
        harvesting_indicator (CharField): A character field to store the harvesting indicator with a maximum length of 255 characters. This field is optional (can be blank).

    Methods:
        __str__(): Returns the string representation of the Harvesting Indicator.

    Meta:
        ordering (list): Specifies the default ordering for the model, which is by 'harvesting_indicator'.
    """

    harvesting_indicator = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.harvesting_indicator

    class Meta:
        ordering = ["harvesting_indicator"]


class HarvestingMean(Base):
    """
    Represents a means of harvesting the seeds.

    This model defines different methods or tools used for harvesting the seeds.
    It inherits from the Base model and contains a single character field for
    the harvesting mean description.

    Attributes:
        harvesting_mean (CharField): A string field (max 100 chars) representing
            the description of the harvesting method. Can be blank.

    Meta:
        ordering: Orders the objects by harvesting_mean field alphabetically.

    Returns:
        str: String representation of the harvesting mean.
    """

    harvesting_mean = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.harvesting_mean

    class Meta:
        ordering = ["harvesting_mean"]


class SeedHead(Base):
    """
    A model representing a seed head type.

    This class extends the Base model and represents different types of seed heads
    in botanical classification.

    Attributes:
        seed_head (CharField): A string field up to 20 characters that stores
            the name or type of the seed head. Can be left blank.

    Meta:
        ordering: Orders instances alphabetically by seed_head field.

    Returns:
        str: String representation of the seed head name.
    """

    seed_head = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.seed_head

    class Meta:
        ordering = ["seed_head"]


class ViablityTest(Base):
    """A model representing a viability test.

    This model stores information about various viability tests that can be performed to determine if the seed is likely to germinate.
    The test name is stored as a character field with a maximum length of 150 characters.

    Attributes:
        viability_test (CharField): The name or description of the viability test,
            limited to 150 characters. Can be blank.

    Meta:
        ordering: Ordered alphabetically by viability_test field
    """

    viability_test = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.viability_test

    class Meta:
        ordering = ["viability_test"]


class SeedStorage(Base):
    """
    A model class representing seed storage information.  Storage information refers to the
    conditions in which seeds are stored before paxking them for distrobution.

    This class inherits from Base and contains details about seed storage locations
    or methods.

    Attributes:
        seed_storage (CharField): Storage information with max length of 150 chars,
            can be left blank.

    Returns:
        str: String representation of the seed storage information.
    """

    seed_storage = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.seed_storage


class OneCultivar(Base):
    """A model representing a single cultivar name to indicate whether a
    plant is a cultivar and can or cannot be distributed.

    This class inherits from Base model and stores individual cultivar names
    with a maximum length of 125 characters.

    Attributes:
        one_cultivar (CharField): The name of the cultivar, allowing blank values
            with maximum 125 characters.

    Meta:
        ordering: Sorts cultivars alphabetically by name

    Returns:
        str: String representation of the cultivar name
    """

    one_cultivar = models.CharField(max_length=125, blank=True)

    def __str__(self) -> str:
        return self.one_cultivar

    class Meta:
        ordering = ["one_cultivar"]


class PackagingMeasure(Base):
    """A model representing a packaging measure used to measure the amount of seeds to be packed in enveloppe.

    This model stores different types of packaging measurements that can be used
    throughout the application.

    Attributes:
        packaging_measure (str): The name or description of the packaging measure.
            Maximum length is 35 characters. Can be blank.

    Example:
        "1 rounded 1/32 teaspoon"
        "A dozen (12) seeds (eyeball)"
    """

    packaging_measure = models.CharField(max_length=35, blank=True)

    def __str__(self) -> str:
        return self.packaging_measure

    class Meta:
        ordering = ["packaging_measure"]


class Dormancy(Base):
    """A model representing plant dormancy characteristics of the seeds prior germination.

    This class defines a database model for storing information about plant dormancy,
    which is the period in a plant's life cycle where growth and development slow or stop.

    Attributes:
        dormancy (str): A CharField storing the dormancy description, max length 50 characters.
                       Can be left blank.

    Returns:
        str: String representation of the dormancy instance, returns the dormancy value.
    """

    dormancy = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.dormancy


class SeedPreparation(Base):
    """
    A model representing seed preparation methods before packing.

    This class stores different types of seed preparation techniques or methods
    used in horticultural or agricultural contexts.

    Attributes:
        seed_preparation (CharField): A string field storing the name or description
            of the seed preparation method, limited to 100 characters.
            Can be left blank.

    Meta:
        ordering: Ordered alphabetically by seed_preparation field.
    """

    seed_preparation = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.seed_preparation

    class Meta:
        ordering = ["seed_preparation"]


class SeedStorageLabelInfo(Base):
    """
    A model representing information stored on seed storage labels which will be attached to the seed enveloppe.

    This model inherits from Base and stores text information that appears on seed storage labels
    up to 50 characters in length. The field is optional (blank=True).

    Attributes:
        seed_storage_label_info (CharField): Text information from seed storage label, max 50 chars

    Methods:
        __str__(): Returns the seed storage label information as a string

    Meta:
        ordering: Orders objects by seed_storage_label_info field
    """

    seed_storage_label_info = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.seed_storage_label_info

    class Meta:
        ordering = ["seed_storage_label_info"]


class SowingDepth(Base):
    """
    A model representing sowing depth measurements for planting.

    This model stores sowing depth information as a string value with a maximum length
    of 25 characters. The sowing depth field is optional (blank=True).

    Attributes:
        sowing_depth (CharField): The depth measurement for sowing, max length 25 chars.

    Returns:
        str: String representation of the sowing depth value

    Meta:
        ordering: Ordered alphabetically by sowing_depth field
    """

    sowing_depth = models.CharField(max_length=25, blank=True)

    def __str__(self) -> str:
        return self.sowing_depth

    class Meta:
        ordering = ["sowing_depth"]


class Lighting(Base):
    """A model for different types of lighting conditions required by the plant for ideal growth.

    This class represents various lighting conditions with their definitions. Each lighting
    condition must be unique and can be described with a definition.

    Attributes:
        lighting (str): The name or type of lighting condition. Must be unique.
            Maximum length of 45 characters. Can be blank.
        definition (str): A description or definition of the lighting condition.
            Maximum length of 75 characters. Can be blank.

    Returns:
        str: A string representation of the lighting condition in the format
            "lighting - definition".
    """

    lighting = models.CharField(unique=True, max_length=45, blank=True)
    definition = models.CharField(max_length=75, blank=True)

    def __str__(self) -> str:
        return f"{self.lighting} - {self.definition}"


class Color(Base):
    """A Color model representing a color entity to be assigned to the flowers of the plant.

    This class inherits from Base and represents a color with a unique name.
    The color name is automatically capitalized when saved.

    Attributes:
        color (CharField): A unique color name, max length 25 characters, can be blank.

    Methods:
        __str__(): Returns the color name as string representation.
        save(*args, **kwargs): Overrides default save to capitalize color name.
    """

    color = models.CharField(unique=True, max_length=25, blank=True)

    def __str__(self) -> str:
        return self.color

    def save(self, *args, **kwargs):
        self.color = self.color.capitalize()
        super().save(*args, **kwargs)


class Habit(Base):
    """A model representing a habit that characterize the plant.

    This class defines a habit with a unique name that can be tracked or associated with other entities.

    Attributes:
        habit (CharField): The name of the habit. Must be unique, limited to 30 characters, and can be blank.

    Meta:
        ordering: Habits are ordered alphabetically by name.

    Returns:
        str: String representation of the habit (the habit name).
    """

    habit = models.CharField(unique=True, max_length=30, blank=True)

    def __str__(self) -> str:
        return self.habit

    class Meta:
        ordering = ["habit"]


class SoilHumidity(Base):
    """A model representing soil humidity requirement that the plant will thrive in.

    This class defines a model for storing soil humidity information, including
    the humidity level category and its corresponding definition.

    Attributes:
        soil_humidity (str): The soil humidity category name (max 45 chars).
        definition (str): Description/definition of the soil humidity category (max 75 chars).
    """

    soil_humidity = models.CharField(max_length=45, blank=True)
    definition = models.CharField(max_length=75, blank=True)

    def __str__(self) -> str:
        return f"{self.soil_humidity} - {self.definition}"


class PlantProfile(Base):
    """A model representing detailed botanical information for a plant species.

    This class stores comprehensive information about plants, including nomenclature,
    physical characteristics, growing conditions, harvesting details, and various
    botanical flags and classifications.

    Attributes:
        latin_name (str): Scientific name of the plant (required, unique, max 75 chars)
        english_name (str): Common English name (optional, max 75 chars)
        french_name (str): Common French name (optional, max 75 chars)
        url (str): Reference URL (optional, max 250 chars)
        light_from (Lighting): Minimum light requirement
        light_to (Lighting): Maximum light requirement
        bloom_start (int): Blooming period start month (0-12)
        bloom_end (int): Blooming period end month (0-12)
        soil_humidity_min (SoilHumidity): Minimum soil moisture requirement
        soil_humidity_max (SoilHumidity): Maximum soil moisture requirement
        min_height (int): Minimum plant height in inches
        max_height (int): Maximum plant height in inches
        size (str): Size category (max 35 chars)
        stratification_detail (str): Stratification process details (max 55 chars)
        stratification_duration (int): Duration of stratification in days
        sowing_depth (SowingDepth): Recommended planting depth
        sowing_period (str): Optimal sowing timeframe (max 55 chars)
        sharing_priority (SharingPriority): Priority level for seed sharing
        harvesting_start (int): Harvest period start month (0-12)
        harvesting_end (int): Harvest period end month (0-12)
        harvesting_indicator (HarvestingIndicator): Indicators for harvest readiness
        harvesting_mean (HarvestingMean): Method of harvest
        seed_head (SeedHead): Type of seed head
        remove_non_seed_material (bool): Whether non-seed material should be removed
        viability_test (ViablityTest): Method for testing seed viability
        seed_storage (SeedStorage): Storage method for seeds
        one_cultivar (OneCultivar): Single cultivar information
        packaging_measure (PackagingMeasure): Packaging size specifications
        dormancy (Dormancy): Seed dormancy duration in days
        seed_preparation (SeedPreparation): Seed preparation method
        hyperlink (str): Related resource link (max 200 chars)
        envelope_label_link (str): Label template link (max 200 chars)
        harvesting_video_link (str): Harvesting instruction video link (max 200 chars)
        seed_picture_link (str): Seed image link (max 200 chars)
        pods_seed_head_picture_link (str): Seed pod image link (max 200 chars)
        seed_storage_label_info (SeedStorageLabelInfo): Storage label information
        notes (str): Additional information (max 450 chars)
        various boolean flags: Multiple boolean indicators for plant characteristics
        flower_color (Color): Color of flowers
        habit (Habit): Growth habit
        taxon (str): Taxonomic classification (max 5 chars) as per VASCAN web site.  Required for VASCAN map presentation
        inaturalist_taxon (str): Taxonomic classification (max 10 chars) as per iNaturalist web site.  Required for iNaturalist map presentation of where the plant is found.

    Methods:
        __str__(): Returns formatted string with plant names and max soil humidity
        compare_heights(): Validates that min_height is less than max_height
        compare_blooming(): Validates blooming period start/end dates
        save(): Overridden save method with custom validation logic
    """

    latin_name = models.CharField(max_length=75, unique=True)
    english_name = models.CharField(max_length=75, blank=True)
    french_name = models.CharField(max_length=75, blank=True)
    url = models.CharField(max_length=250, blank=True)
    light_from = models.ForeignKey(
        Lighting, related_name="light_from", on_delete=models.RESTRICT, blank=True, null=True
    )
    light_to = models.ForeignKey(Lighting, related_name="light_to", on_delete=models.RESTRICT, blank=True, null=True)
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
    harvesting_indicator = models.ForeignKey(HarvestingIndicator, on_delete=models.RESTRICT, null=True, blank=True)
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
    seed_storage_label_info = models.ForeignKey(SeedStorageLabelInfo, on_delete=models.RESTRICT, null=True, blank=True)
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
    drought_tolerant = models.BooleanField(default=False, null=True, blank=True)
    salt_tolerant = models.BooleanField(default=False, null=True, blank=True)
    deer_tolerant = models.BooleanField(default=False, null=True, blank=True)
    easy_to_contain = models.BooleanField(default=False, null=True, blank=True)
    flower_color = models.ForeignKey(Color, on_delete=models.RESTRICT, null=True, blank=True)
    habit = models.ForeignKey(Habit, on_delete=models.RESTRICT, null=True, blank=True)
    taxon = models.CharField(max_length=5, blank=True)
    inaturalist_taxon = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} | {self.latin_name} | {self.english_name} | {self.french_name}| {self.soil_humidity_max}"

    class Meta:
        ordering = ["latin_name"]

    def compare_heights(self):
        """
        Validates that min_height is smaller than max_height for this plant instance.

        Raises:
            ValidationError: If min_height is greater than max_height, raises error with
                            Latin name and height values in message.
        """
        if self.min_height and self.max_height and self.min_height > self.max_height:
            raise ValidationError(
                f"{self.latin_name}: Minimum height ({self.min_height}) must be smaller than maximum height ({self.max_height})"
            )

    def compare_blooming(self):
        """
        Validates blooming period by comparing bloom_start and bloom_end dates.

        This method ensures that:
        1. If bloom_start is None, it's set to 0
        2. If bloom_end is None, both bloom_start and bloom_end are set to 0
        3. If both dates exist, verifies bloom_start occurs before bloom_end

        Raises:
            ValidationError: If bloom_start date is later than bloom_end date
        """
        if not self.bloom_start:
            self.bloom_start = 0
        if not self.bloom_end:
            self.bloom_end = 0
            self.bloom_start = 0
        if self.bloom_start and self.bloom_end and self.bloom_start > self.bloom_end:
            raise ValidationError("Beginning of blooming period must be before end of blooming period")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to handle plant data validation and persistence.

        This method ensures required fields are properly set and validates height and blooming period
        relationships before saving the plant instance to the database.

        Args:
            *args: Variable length argument list to pass to parent save method
            **kwargs: Arbitrary keyword arguments to pass to parent save method

        Raises:
            ValueError: If latin_name field is not provided

        Note:
            - Sets default value of 0 for harvesting_start and harvesting_end if not provided
            - Validates height and blooming period relationships via compare_heights() and compare_blooming()
        """
        if not self.harvesting_start:
            self.harvesting_start = 0
        if not self.harvesting_end:
            self.harvesting_end = 0
        if not self.latin_name:
            raise ValueError("Missing Latin Name")
        self.compare_heights()
        self.compare_blooming()
        super().save(*args, **kwargs)


class ProjectUser(AbstractUser):
    """A custom user model extending Django's AbstractUser.

    This model adds a many-to-many relationship with PlantProfile through
    the PlantCollection intermediary model.

    Attributes:
        plants (ManyToManyField): Collection of PlantProfile objects associated with the user
            through PlantCollection model.

    Example:
        >>> user = ProjectUser.objects.create(username='plantlover')
        >>> user.plants.all()
        <QuerySet []>
    """

    plants = models.ManyToManyField(PlantProfile, through="PlantCollection")

    def __str__(self):
        return str(self.username)


class PlantCollection(models.Model):
    """A model representing a collection of plants owned by users.

    This model creates a relationship between users and plant profiles, allowing users
    to maintain their personal collection of plants with optional details.

    Attributes:
        owner (ForeignKey): Reference to the ProjectUser who owns this plant collection entry.
        plants (ForeignKey): Reference to the PlantProfile being collected.
        details (CharField): Optional additional information about this specific plant collection entry.

    Meta:
        ordering: Ordered by the latin name of the plants.
        constraints: Ensures unique combinations of owner and plants to prevent duplicates.

    Returns:
        str: String representation in the format "owner, plants".
    """

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
    """A model representing morphological elements or characteristics of plants such as flower, leave, seed, etc.

    This model stores various morphological descriptors that can be used to describe
    plant structures or features. Each element is unique and represents a specific
    morphological characteristic.

    Attributes:
        element (CharField): A unique text field (max 75 chars) representing a
            morphological characteristic or feature of a plant.

    Meta:
        ordering: Alphabetically by element name
        verbose_name_plural: "plant morphology"
    """

    element = models.CharField(max_length=75, blank=True, unique=True)

    def __str__(self):
        return self.element

    class Meta:
        ordering = ["element"]
        verbose_name_plural = "plant morphology"


class PlantImage(models.Model):
    """A model representing an image associated with a plant profile.

    This model stores and manages plant images, including their metadata and physical image files.
    It handles image processing on save, automatically resizing images to a standard width while
    maintaining aspect ratio.

    Attributes:
        plant_profile (ForeignKey): Reference to the associated PlantProfile
        morphology_aspect (ForeignKey): Reference to the associated PlantMorphology
        title (str): Title of the image, max length 125 characters
        description (str): Optional description of the image, max length 55 characters
        photo_author (str): Name of the photographer, max length 125 characters
        photo_date (Date): Date when the photo was taken
        image (ImageField): The actual image file, stored in 'project/images'

    Methods:
        save(*args, **kwargs): Overridden save method that handles image processing
            - Deletes old image if being replaced
            - Resizes image to 720px width while maintaining aspect ratio
            - Applies EXIF rotation correction
            - Saves with maximum quality

        get_size(): Returns a dictionary containing the image's dimensions
            Returns:
                dict: Contains 'width' and 'height' keys with pixel values
                int: Returns 0 if the image file is not found

        delete(*args, **kwargs): Overridden delete method that ensures
            proper cleanup of the image file before deleting the model instance
    """

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
        """
        Override the save method to handle image processing before saving a PlantImage instance.

        This method performs the following operations:
        1. Deletes the existing image if it's being replaced
        2. Saves the instance using the parent class's save method
        3. Processes the new image:
            - Corrects image orientation using EXIF data
            - Resizes the image to a target width of 720px while maintaining aspect ratio
            - Saves the processed image with high quality (100)

        Args:
             *args: Variable length argument list for the save method
             **kwargs: Arbitrary keyword arguments for the save method

        Note:
             The method ensures proper cleanup by closing both the PIL Image object
             and the image file after processing.
        """
        try:  # Delete plant if it exists
            this = PlantImage.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except PlantImage.DoesNotExist:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
        img = Image.open(self.image)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        target_width = 720
        h_coefficient = width / target_width
        target_height = height / h_coefficient
        img = img.resize((int(target_width), int(target_height)), Image.LANCZOS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()

    def get_size(self):
        """
        Gets the dimensions of the image associated with this instance.

        Returns:
            dict: A dictionary containing the width and height of the image in pixels.
                  Returns {'width': width, 'height': height} if successful,
                  or 0 if the image file is not found.

        Raises:
            Any other PIL.Image exceptions that may occur when opening the image.
        """
        try:
            img = Image.open(self.image)
        except FileNotFoundError:
            return 0
        width, height = img.size
        img.close()
        size = {"width": width, "height": height}
        return size

    def delete(self, *args, **kwargs):
        """
        Delete project instance and associated image.

        This method overrides the default delete() method to ensure proper cleanup of associated image files
        before deleting the project instance itself.

        Args:
            *args: Variable length argument list to pass to super().delete()
            **kwargs: Arbitrary keyword arguments to pass to super().delete()

        Returns:
            None

        Raises:
            No exceptions are raised as ValueError from image deletion is caught and ignored
        """
        try:
            self.image.delete()
        except ValueError:
            pass
        super().delete(*args, **kwargs)
