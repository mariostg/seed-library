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


class SeedEventTable(Base):
    """
    A model representing a table name where it is possible to find the seeds for a given plant at giveaway events.

    Attributes:
        event_table (CharField): A character field to store the name of the event_table with a maximum length of 100 characters.
            This field is optional (can be blank).

    Methods:
        __str__(): Returns the string representation of the Seed Event Table.

    Meta:
        ordering (list): Specifies the default ordering for the model, which is by 'event_table'.
    """

    seed_event_table = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.seed_event_table

    class Meta:
        ordering = ["seed_event_table"]


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


class FlowerColor(Base):
    """A Color model representing a color entity to be assigned to the flowers of the plant.

    This class inherits from Base and represents a color with a unique name.
    The color name is automatically capitalized when saved.

    Attributes:
        color (CharField): A unique color name, max length 25 characters, can be blank.

    Methods:
        __str__(): Returns the color name as string representation.
        save(*args, **kwargs): Overrides default save to capitalize color name.
    """

    bloom_color = models.CharField(unique=True, max_length=25, blank=True)

    def __str__(self) -> str:
        return self.bloom_color

    def save(self, *args, **kwargs):
        self.bloom_color = self.bloom_color.capitalize()
        super().save(*args, **kwargs)


class GrowthHabit(Base):
    """A model representing a growth habit that characterize the plant.

    This class defines a habit with a unique name that can be tracked or associated with other entities.

    Attributes:
        habit (CharField): The name of the habit. Must be unique, limited to 30 characters, and can be blank.

    Meta:
        ordering: Habits are ordered alphabetically by name.

    Returns:
        str: String representation of the habit (the habit name).
    """

    growth_habit = models.CharField(unique=True, max_length=30, blank=True)

    def __str__(self) -> str:
        return self.growth_habit

    class Meta:
        ordering = ["growth_habit"]


class PlantLifespan(Base):
    """A model representing the lifespan of a plant.

    This class defines the lifecycle of a plant, which can be annual, biennial, or perennial.

    Attributes:
        lifespan (str): The lifespan category of the plant (max 15 chars).

    Returns:
        str: String representation of the lifespan value.
    """

    lifespan = models.CharField(max_length=15, blank=True)

    def __str__(self) -> str:
        return self.lifespan


class ConservationStatus(Base):
    """A model representing the conservation status of a plant.

    This class defines the conservation status of a plant, which can be endangered, threatened, or stable.

    Attributes:
        conservation_status (str): The conservation status of the plant (max 50 chars).

    Returns:
        str: String representation of the conservation status value.
    """

    conservation_status = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.conservation_status


class PlantProfileQuerySet(models.QuerySet):
    def plant_name(self, query):
        """
        Filter plants based on a search query across multiple name fields.

        This method searches for plants where the query string matches partially
        (case-insensitive) with either the Latin, English, or French name.

        Args:
            query (str): The search string to filter plant names.

        Returns:
            QuerySet: A filtered queryset containing plants matching the search criteria.

        Example:
            >>> Plant.objects.plant_name("rose")
            <QuerySet [<Plant: Rosa gallica>, <Plant: Garden rose>, <Plant: Rose trémière>]>
        """
        return self.filter(
            models.Q(latin_name__icontains=query)
            | models.Q(english_name__icontains=query)
            | models.Q(french_name__icontains=query)
        )


class SpreadRate(Base):
    """
    A model representing the spreading rate of a plant.

    The SpreadRate class stores information about how quickly a plant grows
    or spreads in the garden or landscape. This helps in planning proper
    spacing and maintenance requirements for plants.

    Attributes:
        spreading_rate (models.CharField): A string representation of how fast
            a plant spreads, limited to 15 characters. Examples might include
            "Fast", "Moderate", "Slow", etc.
    """

    spreading_rate = models.CharField(max_length=15, blank=True)

    def __str__(self) -> str:
        return self.spreading_rate


class PlantProfile(Base):
    """
    A Django model representing a comprehensive plant profile with botanical, horticultural and ecological attributes.

    This model stores detailed information about plants including:
    - Identification (botanical and common names)
    - Growth characteristics (height, width, habit)
    - Environmental requirements (light, moisture, soil preferences)
    - Cultivation details (blooming periods, harvesting information)
    - Propagation information (seed collection, storage, stratification)
    - Ecological attributes (wildlife benefits, conservation status)
    - Landscape uses (ground cover, container suitability, garden compatibility)
    - Tolerances (drought, salt, wildlife resistance)

    The model implements custom validation for height comparisons and blooming periods,
    and includes specialized query capabilities through a custom manager.

    Attributes:
        latin_name (CharField): Botanical name of the plant (required, unique)
        english_name (CharField): Common name in English (optional)
        french_name (CharField): Common name in French (optional)
        url (CharField): Web reference URL (optional)

        # Light requirements
        full_sun (BooleanField): Whether plant thrives in full sun conditions
        partial_sun (BooleanField): Whether plant thrives in partial sun conditions
        full_shade (BooleanField): Whether plant thrives in full shade conditions

        # Blooming information
        bloom_start (SmallIntegerField): Month when blooming begins (choices from MONTHS)
        bloom_end (SmallIntegerField): Month when blooming ends (choices from MONTHS)
        bloom_color (ForeignKey): Reference to FlowerColor model

        # Moisture preferences
        moisture_dry (BooleanField): Whether plant tolerates dry conditions
        moisture_wet (BooleanField): Whether plant tolerates wet conditions
        moisture_medium (BooleanField): Whether plant prefers medium moisture conditions

        # Plant dimensions
        max_height (FloatField): Maximum mature height
        max_width (FloatField): Maximum mature width/spread

        # Life cycle and growth characteristics
        lifespan (ForeignKey): Reference to PlantLifespan model
        spread_by_rhizome (BooleanField): Whether plant spreads via rhizomes
        dioecious (BooleanField): Whether plant has separate male and female plants
        growth_habit (ForeignKey): Reference to GrowthHabit model

        # Propagation information
        stratification_detail (CharField): Details about cold stratification requirements
        stratification_duration (SmallIntegerField): Duration of stratification in days
        sowing_depth (ForeignKey): Reference to SowingDepth model
        sowing_period (CharField): Description of optimal sowing period
        sharing_priority (ForeignKey): Reference to SharingPriority model

        # Harvesting information
        harvesting_start (SmallIntegerField): Month when harvesting begins (choices from MONTHS)
        harvesting_indicator (ForeignKey): Reference to HarvestingIndicator model
        harvesting_mean (ForeignKey): Reference to HarvestingMean model
        seed_head (ForeignKey): Reference to SeedHead model
        remove_non_seed_material (BooleanField): Whether to remove non-seed material

        # Seed handling
        viability_test (ForeignKey): Reference to ViablityTest model
        seed_storage (ForeignKey): Reference to SeedStorage model
        one_cultivar (ForeignKey): Reference to OneCultivar model
        packaging_measure (ForeignKey): Reference to PackagingMeasure model
        dormancy (ForeignKey): Reference to Dormancy model
        seed_preparation (ForeignKey): Reference to SeedPreparation model
        seed_event_table (ForeignKey): Reference to SeedEventTable model

        # Additional cultivation notes
        seed_cleaning_notes (CharField): Notes on seed cleaning process
        sowing_label_instructions (CharField): Instructions for sowing labels
        sowing_notes (CharField): Detailed notes on sowing process
        envelope_label_link (CharField): Link to envelope label resource
        harvesting_video_link (CharField): Link to harvesting instructional video
        seed_storage_label_info (ForeignKey): Reference to SeedStorageLabelInfo model
        notes (CharField): General notes about the plant
        harvesting_notes (CharField): Detailed notes on harvesting
        toxicity_notes (CharField): Information about plant toxicity
        transplanting_notes (CharField): Notes on transplanting techniques
        alternative_to_notes (CharField): Notes on plants this can replace

        # Gardener-friendly attributes
        germinate_easy (BooleanField): Whether seeds germinate easily
        beginner_friendly (BooleanField): Whether suitable for beginner gardeners
        spreading_rate (ForeignKey): Reference to SpreadRate model

        # Landscape uses
        rock_garden (BooleanField): Suitable for rock gardens
        rain_garden (BooleanField): Suitable for rain gardens
        pond_edge (BooleanField): Suitable for pond edges
        shoreline_rehab (BooleanField): Suitable for shoreline rehabilitation
        container_suitable (BooleanField): Suitable for container gardening
        school_garden_suitable (BooleanField): Suitable for school gardens
        ground_cover (BooleanField): Functions as ground cover
        garden_edge (BooleanField): Suitable for garden edges
        woodland_garden (BooleanField): Suitable for woodland gardens
        wind_break_hedge (BooleanField): Suitable as windbreak or hedge
        erosion_control (BooleanField): Helps with erosion control
        seed_availability (BooleanField): Seeds are readily available
        accepting_seed (BooleanField): Whether accepting seeds for this plant
        keystones_species (BooleanField): Whether considered a keystone species

        # Tolerances
        drought_tolerant (BooleanField): Tolerant of drought conditions
        salt_tolerant (BooleanField): Tolerant of salty conditions
        deer_tolerant (BooleanField): Resistant to deer damage
        rabbit_tolerant (BooleanField): Resistant to rabbit damage
        foot_traffic_tolerant (BooleanField): Tolerant of foot traffic
        limestone_tolerant (BooleanField): Tolerant of limestone soils
        sand_tolerant (BooleanField): Tolerant of sandy soils
        acidic_soil_tolerant (BooleanField): Tolerant of acidic soils
        boulevard_tolerant (BooleanField): Suitable for boulevard plantings
        juglone_tolerant (BooleanField): Tolerant of juglone (walnut toxin)
        transplantation_tolerant (BooleanField): Tolerates transplanting well

        # Ecological benefits
        hummingbird_friendly (BooleanField): Attracts hummingbirds
        butterfly_friendly (BooleanField): Attracts butterflies
        bee_friendly (BooleanField): Beneficial for bees
        bird_friendly (BooleanField): Beneficial for birds
        nitrogen_fixer (BooleanField): Plant fixes nitrogen in soil
        easy_to_contain (BooleanField): Plant is easy to contain/not invasive
        cedar_hedge_replacement (BooleanField): Can replace cedar hedges

        # Caution attributes
        cause_dermatitis (BooleanField): Can cause skin irritation
        produces_burs (BooleanField): Produces burrs that stick to clothing/fur

        # Taxonomic and visual characteristics
        taxon (CharField): Taxonomic classification code
        conservation_status (ForeignKey): Reference to ConservationStatus model
        inaturalist_taxon (CharField): iNaturalist taxonomic identifier
    """

    latin_name = models.CharField(max_length=75, unique=True)
    english_name = models.CharField(max_length=75, blank=True)
    french_name = models.CharField(max_length=75, blank=True)
    url = models.CharField(max_length=250, blank=True)

    # We use 3 levels of light to define the light requirement of the plant
    full_sun = models.BooleanField(default=False, null=True, blank=True)
    partial_sun = models.BooleanField(default=False, null=True, blank=True)
    full_shade = models.BooleanField(default=False, null=True, blank=True)

    bloom_start = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    bloom_end = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
    moisture_dry = models.BooleanField(default=False, null=True, blank=True)
    moisture_wet = models.BooleanField(default=False, null=True, blank=True)
    moisture_medium = models.BooleanField(default=False, null=True, blank=True)
    max_height = models.FloatField(blank=True, null=True, default=0)
    max_width = models.FloatField(blank=True, null=True, default=0)
    lifespan = models.ForeignKey(PlantLifespan, on_delete=models.RESTRICT, blank=True, null=True)
    spread_by_rhizome = models.BooleanField(default=False, null=True, blank=True)
    dioecious = models.BooleanField(default=False, null=True, blank=True)

    stratification_detail = models.CharField(max_length=55, blank=True)
    stratification_duration = models.SmallIntegerField(blank=True, null=True, default=0)
    sowing_depth = models.ForeignKey(SowingDepth, on_delete=models.RESTRICT, blank=True, null=True)
    sowing_period = models.CharField(max_length=55, blank=True)
    sharing_priority = models.ForeignKey(SharingPriority, on_delete=models.RESTRICT, blank=True, null=True)
    harvesting_start = models.SmallIntegerField(choices=MONTHS.items(), blank=True, default=0)
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
    seed_cleaning_notes = models.CharField(max_length=70, blank=True)
    sowing_label_instructions = models.CharField(max_length=40, blank=True)
    sowing_notes = models.CharField(max_length=450, blank=True)
    envelope_label_link = models.CharField(max_length=200, blank=True)
    harvesting_video_link = models.CharField(max_length=200, blank=True)
    seed_storage_label_info = models.ForeignKey(SeedStorageLabelInfo, on_delete=models.RESTRICT, null=True, blank=True)
    seed_event_table = models.ForeignKey(SeedEventTable, on_delete=models.RESTRICT, null=True, blank=True)
    notes = models.CharField(max_length=450, blank=True)
    harvesting_notes = models.CharField(max_length=450, blank=True)
    toxicity_notes = models.CharField(max_length=450, blank=True)
    transplanting_notes = models.CharField(max_length=450, blank=True)
    alternative_to_notes = models.CharField(max_length=450, blank=True)

    germinate_easy = models.BooleanField(default=False, null=True, blank=True)
    beginner_friendly = models.BooleanField(default=False, null=True, blank=True)
    spreading_rate = models.ForeignKey(SpreadRate, on_delete=models.RESTRICT, null=True, blank=True)
    rock_garden = models.BooleanField(default=False, null=True, blank=True)
    rain_garden = models.BooleanField(default=False, null=True, blank=True)
    pond_edge = models.BooleanField(default=False, null=True, blank=True)
    shoreline_rehab = models.BooleanField(default=False, null=True, blank=True)
    container_suitable = models.BooleanField(default=False, null=True, blank=True)
    school_garden_suitable = models.BooleanField(default=False, null=True, blank=True)
    ground_cover = models.BooleanField(default=False, null=True, blank=True)
    garden_edge = models.BooleanField(default=False, null=True, blank=True)
    woodland_garden = models.BooleanField(default=False, null=True, blank=True)
    wind_break_hedge = models.BooleanField(default=False, null=True, blank=True)
    erosion_control = models.BooleanField(default=False, null=True, blank=True)
    seed_availability = models.BooleanField(default=False, null=True, blank=True)

    accepting_seed = models.BooleanField(default=False, null=True, blank=True)
    keystones_species = models.BooleanField(default=False, null=True, blank=True)

    drought_tolerant = models.BooleanField(default=False, null=True, blank=True)
    salt_tolerant = models.BooleanField(default=False, null=True, blank=True)
    deer_tolerant = models.BooleanField(default=False, null=True, blank=True)
    rabbit_tolerant = models.BooleanField(default=False, null=True, blank=True)
    foot_traffic_tolerant = models.BooleanField(default=False, null=True, blank=True)
    limestone_tolerant = models.BooleanField(default=False, null=True, blank=True)
    sand_tolerant = models.BooleanField(default=False, null=True, blank=True)
    acidic_soil_tolerant = models.BooleanField(default=False, null=True, blank=True)
    hummingbird_friendly = models.BooleanField(default=False, null=True, blank=True)
    butterfly_friendly = models.BooleanField(default=False, null=True, blank=True)
    bee_friendly = models.BooleanField(default=False, null=True, blank=True)
    bird_friendly = models.BooleanField(default=False, null=True, blank=True)
    boulevard_tolerant = models.BooleanField(default=False, null=True, blank=True)
    juglone_tolerant = models.BooleanField(default=False, null=True, blank=True)
    transplantation_tolerant = models.BooleanField(default=False, null=True, blank=True)
    nitrogen_fixer = models.BooleanField(default=False, null=True, blank=True)
    easy_to_contain = models.BooleanField(default=False, null=True, blank=True)
    cedar_hedge_replacement = models.BooleanField(default=False, null=True, blank=True)
    cause_dermatitis = models.BooleanField(default=False, null=True, blank=True)
    produces_burs = models.BooleanField(default=False, null=True, blank=True)

    bloom_color = models.ForeignKey(FlowerColor, on_delete=models.RESTRICT, null=True, blank=True)
    growth_habit = models.ForeignKey(GrowthHabit, on_delete=models.RESTRICT, null=True, blank=True)
    taxon = models.CharField(max_length=5, blank=True)
    conservation_status = models.ForeignKey(ConservationStatus, on_delete=models.RESTRICT, null=True, blank=True)
    inaturalist_taxon = models.CharField(max_length=10, blank=True)

    search_plant = PlantProfileQuerySet.as_manager()
    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.pk} | {self.latin_name} | {self.english_name} | {self.french_name}"

    class Meta:
        ordering = ["latin_name"]

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
            - Sets default value of 0 for harvesting_start if not provided
            - Validates height and blooming period relationships via compare_heights() and compare_blooming()
        """
        if not self.harvesting_start:
            self.harvesting_start = 0
        if not self.latin_name:
            raise ValueError("Missing Latin Name")
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
