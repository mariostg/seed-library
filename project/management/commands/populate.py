"""
Typical usage:
    python manage.py populate

Populate command uses the data available from the test-data folder.  This folder contains all the CSV files necessary to set up the system initially.

!!! warning
    It will overwrite all existing data in the system.

"""

import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from main.settings import DEBUG
from project import models


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            action="store",
            help="Specify the path of the csv file to use as data source.",
        )

    def handle(self, *args, filepath, **options):
        if (
            not DEBUG
        ):  # Don't populate the database in production except for initial deployment
            self.stdout.write(
                self.style.WARNING("This command is only available in DEBUG mode")
            )
            return  # Exit early instead of raising an exception

        self.filepath = Path(filepath)
        self.latin_names = models.PlantProfile.objects.values_list(
            "latin_name", flat=True
        )  # Get existing latin names from the database. It will be populated again if import_latin_names is called.

        if not self.filepath.exists():
            raise FileNotFoundError(
                f"The specified filepath does not exist: {self.filepath}"
            )
        if not self.filepath.is_dir():
            raise NotADirectoryError(
                f"The specified filepath is not a directory: {self.filepath}"
            )

        # this is the list of csv files that will be used to populate the database.
        self.csv_files = {
            "latin_names": "plant-names-latin - csv.csv",
            "english_names": "plant-names-english - csv.csv",
            "french_names": "plant-names-french - csv.csv",
            "bird_friendly": "plant-bird-friendly - csv.csv",
            "boulevard_garden_tolerant": "plant-boulevard-garden-tolerant - csv.csv",
            "pollinator_garden": "plant-pollinator-garden - csv.csv",
            "butterfly_host": "plant-butterfly-host - csv.csv",
            "bee_host": "plant-bee-host - csv.csv",
            "cause_dermatitis": "plant-cause-dermatitis - csv.csv",
            "hedge": "plant-hedge - csv.csv",
            "bloom_color": "plant-bloom-color - csv.csv",
            "conservation_status": "plant-conservation-status - csv.csv",
            "container_suitable": "plant-container-suitable - csv.csv",
            "drought_tolerant": "plant-drought-tolerant - csv.csv",
            "germinate_easy": "plant-germinate-easy - csv.csv",
            "ground_cover": "plant-ground-cover - csv.csv",
            "growth_habit": "plant-growth-habit - csv.csv",
            "hummingbird_friendly": "plant-hummingbird-friendly - csv.csv",
            "juglone_tolerant": "plant-juglone-tolerant - csv.csv",
            "keystones_species": "plant-keystones-species - csv.csv",
            "lifespan": "plant-lifespan - csv.csv",
            "limestone_tolerant": "plant-limestone-tolerant - csv.csv",
            "max-height": "plant-max-height - csv.csv",
            "max-width": "plant-max-width - csv.csv",
            "nitrogen_fixer": "plant-nitrogen-fixer - csv.csv",
            "on_cultivar": "plant-on-cultivar - csv.csv",
            "packaging_measure": "plant-packaging-measure - csv.csv",
            "plant-taxon": "plant-taxon - csv.csv",
            "produces-burs": "plant-produces-burs - csv.csv",
            "salt_tolerant": "plant-salt-tolerant - csv.csv",
            "sand_tolerant": "plant-sand-tolerant - csv.csv",
            "school_garden": "plant-school-garden - csv.csv",
            "seed_head": "plant-seed-head - csv.csv",
            "shoreline_rehab": "plant-shoreline-rehab - csv.csv",
            "sowing-depth": "plant-sowing-depth - csv.csv",
            "stratification_duration": "plant-stratification-duration - csv.csv",
            "transplantation_tolerant": "plant-transplantation-tolerant - csv.csv",
            "beginner_friendly": "plant-beginner-friendly - csv.csv",
            "moisture-dry": "plant-moisture-dry - csv.csv",
            "moisture-medium": "plant-moisture-medium - csv.csv",
            "moisture-wet": "plant-moisture-wet - csv.csv",
            "full-sun": "plant-full-sun - csv.csv",
            "part-shade": "plant-part-shade - csv.csv",
            "full-shade": "plant-full-shade - csv.csv",
            "spread-by-rhizome": "plant-spread-by-rhizome - csv.csv",
            "dioecious": "plant-dioecious - csv.csv",
            "seed-event-table": "plant-seed-event-table - csv.csv",
            "rock-garden": "plant-rock-garden - csv.csv",
            "septic-tank-safe": "plant-septic-tank-safe - csv.csv",
            "wetland-garden": "plant-wetland-garden - csv.csv",
            "grasp-candidate": "plant-grasp-candidate - csv.csv",
            "toxicity_indicator": "plant-toxicity-indicator - csv.csv",
            "toxicity_indicator_notes": "plant-toxicity-indicator-notes - csv.csv",
            "acidic_soil_tolerant": "plant-acidic-soil-tolerant - csv.csv",
            "grasp_candidate_notes": "plant-grasp-candidate-notes - csv.csv",
            "self_seeding": "plant-self-seeding - csv.csv",
            "does_not_spread": "plant-does-not-spread - csv.csv",
            "sharing_priority": "plant-sharing-priority - csv.csv",
            "bloom_start": "plant-bloom-start - csv.csv",
            "bloom_end": "plant-bloom-end - csv.csv",
            "rabbit_tolerant": "plant-rabbit-tolerant - csv.csv",
            "deer_tolerant": "plant-deer-tolerant - csv.csv",
            "rain_garden": "plant-rain-garden - csv.csv",
            "woodland_garden": "plant-woodland-garden - csv.csv",
            "native_to_ottawa_region": "plant-native-to-ottawa-region - csv.csv",
            "harvesting_start": "plant-harvesting-start - csv.csv",
            "seed_viability_test": "plant-seed-viability-test - csv.csv",
            "harvesting_indicator": "plant-harvesting-indicator - csv.csv",
            "harvesting_mean": "plant-harvesting-mean - csv.csv",
            "remove_non_seed_material": "plant-remove-non-seed-material - csv.csv",
            "seed_storage": "plant-seed-storage - csv.csv",
        }

        # Clear existing data in the database
        models.PlantProfile.all_objects.all().delete()
        models.BloomColor.objects.all().delete()
        models.ConservationStatus.objects.all().delete()
        models.ConservationStatus.objects.all().delete()
        models.Dormancy.objects.all().delete()
        models.GrowthHabit.objects.all().delete()
        models.HarvestingIndicator.objects.all().delete()
        models.HarvestingMean.objects.all().delete()
        models.Lighting.objects.all().delete()
        models.OneCultivar.objects.all().delete()
        models.PackagingMeasure.objects.all().delete()
        models.PlantLifespan.objects.all().delete()
        models.SeedHead.objects.all().delete()
        models.SeedPreparation.objects.all().delete()
        models.SeedStorage.objects.all().delete()
        models.SeedStorageLabelInfo.objects.all().delete()
        models.SharingPriority.objects.all().delete()
        models.SowingDepth.objects.all().delete()
        models.SeedViabilityTest.objects.all().delete()
        models.SeedEventTable.objects.all().delete()
        models.ToxicityIndicator.objects.all().delete()
        models.ButterflySpecies.objects.all().delete()

        # we start by inserting the latin names of plants.
        # This is a unique key and must be done first.
        self.import_latin_names()
        self.import_english_names()
        self.import_french_names()
        self.import_bloom_color()
        self.import_conservation_status()
        self.import_growth_habit()
        self.import_height()
        self.import_lifespan()
        self.import_on_cultivar()
        self.import_packaging_measure()
        self.import_seed_head()
        self.import_sowing_depth()
        self.import_stratification_duration()
        self.import_taxon()
        self.import_width()
        self.import_seed_event_table()
        self.import_toxicity_indicator()
        self.import_toxicity_indicator_notes()
        self.import_grasp_candidate_notes()
        self.import_sharing_priority()
        self.import_seed_viability_test()
        self.import_harvesting_indicator()
        self.import_harvesting_mean()
        self.import_seed_storage()
        self.import_bloom_start()
        self.import_bloom_end()

        # Insert the boolean fields.
        # Define a mapping of model field names to CSV filenames
        boolean_fields = {
            "bee_host": "bee_host",
            "pollinator_garden": "pollinator_garden",
            "butterfly_host": "butterfly_host",
            "hummingbird_friendly": "hummingbird_friendly",
            "container_suitable": "container_suitable",
            "ground_cover": "ground_cover",
            "shoreline_rehab": "shoreline_rehab",
            "drought_tolerant": "drought_tolerant",
            "salt_tolerant": "salt_tolerant",
            "sand_tolerant": "sand_tolerant",
            "keystones_species": "keystones_species",
            "nitrogen_fixer": "nitrogen_fixer",
            "germinate_easy": "germinate_easy",
            "boulevard_garden_tolerant": "boulevard_garden_tolerant",
            "bird_friendly": "bird_friendly",
            "hedge": "hedge",
            "juglone_tolerant": "juglone_tolerant",
            "cause_dermatitis": "cause_dermatitis",
            "produces_burs": "produces-burs",
            "transplantation_tolerant": "transplantation_tolerant",
            "limestone_tolerant": "limestone_tolerant",
            "school_garden": "school_garden",
            "beginner_friendly": "beginner_friendly",
            "moisture_dry": "moisture-dry",
            "moisture_medium": "moisture-medium",
            "moisture_wet": "moisture-wet",
            "full_sun": "full-sun",
            "part_shade": "part-shade",
            "full_shade": "full-shade",
            "spread_by_rhizome": "spread-by-rhizome",
            "dioecious": "dioecious",
            "rock_garden": "rock-garden",
            "septic_tank_safe": "septic-tank-safe",
            "wetland_garden": "wetland-garden",
            "grasp_candidate": "grasp-candidate",
            "acidic_soil_tolerant": "acidic_soil_tolerant",
            "self_seeding": "self_seeding",
            "does_not_spread": "does_not_spread",
            "rabbit_tolerant": "rabbit_tolerant",
            "deer_tolerant": "deer_tolerant",
            "rain_garden": "rain_garden",
            "woodland_garden": "woodland_garden",
            "remove_non_seed_material": "remove_non_seed_material",
            "native_to_ottawa_region": "native_to_ottawa_region",
        }

        # Update all boolean fields using a loop
        for field_name, csv_filename in boolean_fields.items():
            self.stdout.write(self.style.SUCCESS(f"\n>>>Processing {field_name}..."))
            try:
                self.update_boolean_field(
                    models.PlantProfile, field_name, self.csv_files[csv_filename]
                )
            except KeyError:
                self.stdout.write(
                    self.style.ERROR(
                        f"CSV file not found: {csv_filename} during processing {field_name}"
                    )
                )
                exit(1)

        self.set_actaea_racemosa_boolean_fields()

    def check_latin_names_in_csv(self, filename):
        """
        Check if the latin names in the CSV file exist in the database.

        Args:
            filename: The name of the CSV file to check

        Returns:
            tuple: (existing_names, missing_names) - lists of names that exist and don't exist in the database
        """
        filepath = self.filepath / filename
        existing_names = []
        missing_names = []

        self.stdout.write(self.style.SUCCESS(f"Checking latin names in {filename}..."))
        try:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "latin_name" not in row:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Row missing 'latin_name' field in {filename}"
                            )
                        )
                        continue

                    latin_name = row["latin_name"].capitalize()
                    if latin_name in self.latin_names:
                        existing_names.append(latin_name)
                    else:
                        missing_names.append(latin_name)

            if missing_names:
                self.stdout.write(
                    self.style.WARNING(
                        f"Found {len(missing_names)} latin names in {filename} that don't exist in the database: "
                        f"{', '.join(missing_names[:5])}"
                        + ("..." if len(missing_names) > 5 else "")
                    )
                )
            return existing_names, missing_names

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {filepath}"))
            return [], []
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error checking latin names in {filename}: {str(e)}")
            )
            return [], []

    def unique_values(self, filename, field_name):
        """Read a CSV file and return unique values for a specified field."""
        filepath = self.filepath / filename
        unique_values_set = set()

        try:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    value = row.get(field_name)
                    if value:
                        unique_values_set.add(value.strip())
            return unique_values_set
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {filepath}"))
            return set()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error processing {filename}: {str(e)}")
            )
            return set()

    def insert_unique_values(
        self, model_class: models, field_name: str, unique_values_set: set
    ):
        """Insert unique values into a specified model field.

        Returns:
            int: The number of values successfully inserted.
        """
        inserted_count = 0
        for value in unique_values_set:
            if value:
                try:
                    obj, created = model_class.objects.get_or_create(
                        **{field_name: value}
                    )
                    if created:
                        inserted_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Inserted {field_name}: {value}")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"{field_name} already exists: {value}")
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error inserting {field_name} '{value}': {str(e)}"
                        )
                    )
        return inserted_count

    def _update_vernacular_plant_name(self, filename, field_name, model_class=None):
        """
        Updates a specified attribute for plant profiles from a CSV file.

        This method reads data from a CSV file and updates the specified field
        for PlantProfile instances that match the latin_name in the CSV.
        Optionally accepts a different model class to use for the updates.

        Parameters:
        ----------
        filename : str
            The name of the CSV file containing plant data.
        field_name : str
            The name of the field/attribute to update in the PlantProfile model.
        model_class : Django model class, optional
            The model class to use for updates. If None, defaults to PlantProfile.
            When a different model is provided, it first inserts unique values from the file.

        Notes:
        -----
        The CSV file must contain at least 'latin_name' and the specified field_name columns.
        The method reports success/failure statistics to stdout using Django's command styling.

        Raises:
        ------
        FileNotFoundError: When the specified CSV file doesn't exist
        Exception: For any other errors that occur during processing
        """
        if model_class is None:
            model_class = models.PlantProfile
        else:
            self.insert_unique_values(
                model_class, field_name, self.unique_values(filename, field_name)
            )

        filepath = self.filepath / filename
        try:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                updated_count = 0
                missing_count = 0

                for row in reader:
                    if "latin_name" not in row or field_name not in row:
                        self.stdout.write(
                            self.style.WARNING(f"Row missing required fields: {row}")
                        )
                        continue

                    latin_name = row["latin_name"].capitalize()
                    name_value = row[field_name]
                    try:
                        plant = models.PlantProfile.objects.get(latin_name=latin_name)
                        setattr(plant, field_name, name_value)
                        plant.save()
                        updated_count += 1
                    except model_class.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Plant with latin name '{latin_name}' does not exist"
                            )
                        )
                        missing_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated {updated_count} plant {field_name}s, {missing_count} plants not found"
                    )
                )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {filepath}"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error processing {filename}: {str(e)}")
            )

    def import_latin_names(self):
        self.stdout.write(
            self.style.SUCCESS("Starting to populate the database with plant data...")
        )
        """read csv file and insert latin names into the PlantProfile model."""
        filepath = self.filepath / self.csv_files["latin_names"]
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                latin_name = row.get("latin_name")
                if latin_name:
                    plant, created = models.PlantProfile.objects.get_or_create(
                        latin_name=latin_name
                    )
                    if not created:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Latin name already exists: {latin_name}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR("Row missing 'latin_name' field")
                    )
        self.latin_names = models.PlantProfile.objects.values_list(
            "latin_name", flat=True
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {len(self.latin_names)} latin names in database from file ."
            )
        )

    def import_english_names(self):
        """Read the english names CSV file and update the PlantProfile model with english names."""
        eng_exist, eng_missing = self.check_latin_names_in_csv(
            self.csv_files["english_names"]
        )
        self._update_vernacular_plant_name(
            self.csv_files["english_names"], "english_name"
        )

    def import_french_names(self):
        """Read the french names CSV file and update the PlantProfile model with french names."""
        fr_exist, fr_missing = self.check_latin_names_in_csv(
            self.csv_files["french_names"]
        )
        self._update_vernacular_plant_name(
            self.csv_files["french_names"], "french_name"
        )

    def import_taxon(self):
        """Read the plant taxon CSV file and update the PlantProfile model with taxon values."""
        taxon_exist, taxon_missing = self.check_latin_names_in_csv(
            self.csv_files["plant-taxon"]
        )
        self._update_vernacular_plant_name(self.csv_files["plant-taxon"], "taxon")

    def import_height(self):
        """Read the plant max height CSV file and update the PlantProfile model with height values."""
        height_exist, height_missing = self.check_latin_names_in_csv(
            self.csv_files["max-height"]
        )
        self._update_vernacular_plant_name(self.csv_files["max-height"], "max_height")

    def import_width(self):
        """Read the plant max width CSV file and update the PlantProfile model with width values."""
        width_exist, width_missing = self.check_latin_names_in_csv(
            self.csv_files["max-width"]
        )
        self._update_vernacular_plant_name(self.csv_files["max-width"], "max_width")

    def import_bloom_start(self):
        """Read the plant bloom start CSV file and update the PlantProfile model with bloom start values."""
        bloom_start_exist, bloom_start_missing = self.check_latin_names_in_csv(
            self.csv_files["bloom_start"]
        )
        self._update_vernacular_plant_name(self.csv_files["bloom_start"], "bloom_start")

    def import_bloom_end(self):
        """Read the plant bloom end CSV file and update the PlantProfile model with bloom end values."""
        bloom_end_exist, bloom_end_missing = self.check_latin_names_in_csv(
            self.csv_files["bloom_end"]
        )
        self._update_vernacular_plant_name(self.csv_files["bloom_end"], "bloom_end")

    def import_harvesting_start(self):
        """Read the plant harvesting start CSV file and update the PlantProfile model with harvesting start values."""
        harvesting_start_exist, harvesting_start_missing = (
            self.check_latin_names_in_csv(self.csv_files["harvesting_start"])
        )
        self._update_vernacular_plant_name(
            self.csv_files["harvesting_start"], "harvesting_start"
        )

    def import_sharing_priority(self):
        """Read the plant sharing priority CSV file and update the PlantProfile model with sharing priority values."""
        self._update_vernacular_plant_name(
            self.csv_files["sharing_priority"],
            "sharing_priority",
            models.SharingPriority,
        )

    def import_stratification_duration(self):
        """Read the plant max stratification_duertion CSV file and update the PlantProfile model with width values."""
        stratification_duration_exist, stratification_duration_missing = (
            self.check_latin_names_in_csv(self.csv_files["stratification_duration"])
        )
        self._update_vernacular_plant_name(
            self.csv_files["stratification_duration"], "stratification_duration"
        )

    def import_grasp_candidate_notes(self):
        grasp_candidate_notes_exist, grasp_candidate_notes_missing = (
            self.check_latin_names_in_csv(self.csv_files["stratification_duration"])
        )
        """Read the plant grasp candidate notes CSV file and update the PlantProfile model with notes."""
        self._update_vernacular_plant_name(
            self.csv_files["grasp_candidate_notes"], "grasp_candidate_notes"
        )

    def import_toxicity_indicator_notes(self):
        """Read the plant toxicity indicator notes CSV file and update the PlantProfile model with notes."""
        toxicity_indicator_notes_exist, toxicity_indicator_notes_missing = (
            self.check_latin_names_in_csv(self.csv_files["toxicity_indicator_notes"])
        )
        self._update_vernacular_plant_name(
            self.csv_files["toxicity_indicator_notes"], "toxicity_indicator_notes"
        )

    def import_seed_head(self):
        """Read the plant seed head CSV file and update the SeedHead model with seed head values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["seed_head"],
            field_name="seed_head",
            model_class=models.SeedHead,
            display_name="Seed head",
        )

    def import_seed_viability_test(self):
        """Read the plant seed viability test CSV file and update the PlantProfile model with seed viability values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["seed_viability_test"],
            field_name="seed_viability_test",
            model_class=models.SeedViabilityTest,
            display_name="Seed viability test",
        )

    def import_harvesting_indicator(self):
        """Read the plant harvesting indicator CSV file and update the PlantProfile model with harvesting indicator values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["harvesting_indicator"],
            field_name="harvesting_indicator",
            model_class=models.HarvestingIndicator,
            display_name="Harvesting indicator",
        )

    def import_harvesting_mean(self):
        """Read the plant harvesting mean CSV file and update the PlantProfile model with harvesting mean values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["harvesting_mean"],
            field_name="harvesting_mean",
            model_class=models.HarvestingMean,
            display_name="Harvesting mean",
        )

    def import_seed_storage(self):
        """Read the plant seed storage CSV file and update the PlantProfile model with seed storage values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["seed_storage"],
            field_name="seed_storage",
            model_class=models.SeedStorage,
            display_name="Seed storage",
        )

    def import_bloom_color(self):
        """Read the plant color CSV file and update the PlantProfile model with color values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["bloom_color"],
            field_name="bloom_color",
            model_class=models.BloomColor,
            display_name="Color",
        )

    def import_on_cultivar(self):
        """Read the on cultivar CSV file and update the PlantProfile model with on cultivar values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["on_cultivar"],
            field_name="on_cultivar",
            model_class=models.OneCultivar,
            display_name="On cultivar",
        )

    def import_packaging_measure(self):
        self.import_foreign_key_relation(
            csv_file=self.csv_files["packaging_measure"],
            field_name="packaging_measure",
            model_class=models.PackagingMeasure,
            display_name="Packaging measure",
        )

    def import_nitrogen_fixer(self):
        self.import_foreign_key_relation(
            csv_file=self.csv_files["nitrogen_fixer"],
            field_name="nitrogen_fixer",
            model_class=models.NitrogenFixer,
            display_name="Nitrogen fixer",
        )

    def import_lifespan(self):
        self.import_foreign_key_relation(
            csv_file=self.csv_files["lifespan"],
            field_name="lifespan",
            model_class=models.PlantLifespan,
            display_name="Plant lifespan",
        )

    def import_conservation_status(self):
        self.import_foreign_key_relation(
            csv_file=self.csv_files["conservation_status"],
            field_name="conservation_status",
            model_class=models.ConservationStatus,
            display_name="Conservation status",
        )

    def import_growth_habit(self):
        """Read the growth habit CSV file and update the PlantProfile model with growth habit values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["growth_habit"],
            field_name="growth_habit",
            model_class=models.GrowthHabit,
            display_name="Growth habit",
        )

    def import_sowing_depth(self):
        """Read the sowing depth CSV file and update the SowingDepth model with sowing depth values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["sowing-depth"],
            field_name="sowing_depth",
            model_class=models.SowingDepth,
            display_name="Sowing depth",
        )

    def import_seed_event_table(self):
        """Read the seed event table CSV file and update the SeedEventTable model with seed event values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["seed-event-table"],
            field_name="seed_event_table",
            model_class=models.SeedEventTable,
            display_name="Seed event table",
        )

    def import_toxicity_indicator(self):
        """Read the toxicity indicator CSV file and update the PlantProfile model with toxicity values."""
        self.import_foreign_key_relation(
            csv_file=self.csv_files["toxicity_indicator"],
            field_name="toxicity_indicator",
            model_class=models.ToxicityIndicator,
            display_name="Toxicity indicator",
        )

    def import_foreign_key_relation(
        self, csv_file, field_name, model_class, display_name=None
    ):
        """
        Generic method to import values for a foreign key relation from a CSV file.

        Args:
            csv_file: Name of the CSV file containing the data
            field_name: Name of the field in both CSV and model
            model_class: The Django model class for the foreign key
            display_name: Human-readable name for logging (defaults to field_name)
        """
        if display_name is None:
            display_name = field_name.replace("_", " ").title()

        # Check if latin names in the CSV exist in the database
        existing_names, missing_names = self.check_latin_names_in_csv(csv_file)

        # Get unique values and insert them into the related model
        unique_values = self.unique_values(csv_file, field_name)
        inserted_count = self.insert_unique_values(
            model_class, field_name, unique_values
        )
        self.stdout.write(
            self.style.SUCCESS(f"{display_name} values inserted successfully.\n")
        )

        if inserted_count > 0:
            filepath = self.filepath / csv_file
            try:
                with open(filepath, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    updated_count = 0
                    missing_count = 0

                    for row in reader:
                        if "latin_name" not in row or field_name not in row:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Row missing required fields: {row}"
                                )
                            )
                            continue

                        latin_name = row["latin_name"].capitalize()
                        relation_value = row[field_name].strip()

                        try:
                            plant = models.PlantProfile.objects.get(
                                latin_name=latin_name
                            )
                            relation_instance = model_class.objects.get(
                                **{field_name: relation_value}
                            )
                            setattr(plant, field_name, relation_instance)
                            plant.save()
                            updated_count += 1
                        except models.PlantProfile.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Plant with latin name '{latin_name}' does not exist"
                                )
                            )
                            missing_count += 1
                        except model_class.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"{display_name} '{relation_value}' does not exist for {latin_name}"
                                )
                            )
                            missing_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated {updated_count} plants with {display_name.lower()} values, {missing_count} updates failed"
                        )
                    )
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"CSV file not found: {filepath}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing {display_name.lower()} CSV file: {str(e)}"
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(f"{display_name} values set successfully.\n")
            )

    def update_boolean_field(self, model_class, field_name, csv_file):
        """
        Generic method to update boolean fields in a model from a CSV file.

        Args:
            model_class: The Django model class to update
            field_name: The name of the boolean field to update
            csv_file: The CSV filename to use for data
        """
        exist_names, missing_names = self.check_latin_names_in_csv(csv_file)
        filepath = self.filepath / csv_file
        self.stdout.write(self.style.SUCCESS(f"Updating {field_name} attributes..."))
        try:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                updated_count = 0
                missing_count = 0

                for row in reader:
                    if "latin_name" not in row or field_name not in row:
                        self.stdout.write(
                            self.style.WARNING(f"Row missing required fields: {row}")
                        )
                        continue

                    latin_name = row["latin_name"].capitalize()
                    field_value = row[field_name]

                    # Convert string values to boolean
                    boolean_value = field_value.lower() in ("yes", "true")
                    try:
                        plant = model_class.objects.get(latin_name=latin_name)
                        setattr(plant, field_name, boolean_value)
                        plant.save()
                        updated_count += 1
                    except model_class.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Plant with latin name '{latin_name}' does not exist"
                            )
                        )
                        missing_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated {updated_count} plants with {field_name} attributes, {missing_count} plants not found"
                    )
                )

                # Report counts for true/false values
                true_count = model_class.objects.filter(**{field_name: True}).count()
                false_count = model_class.objects.filter(**{field_name: False}).count()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{field_name.replace('_', ' ').title()} plants: {true_count}\n"
                        f"Non-{field_name.replace('_', ' ')} plants: {false_count}"
                    )
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {filepath}"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error processing {field_name} CSV file: {str(e)}")
            )

    # a function to set to true the boolean fields of the plant profile of actaea racemosa.
    # refer to boolean_fields dictionary
    # in the populate.py file for the list of fields to set.
    # This shall not be used in production, but only for testing purposes.
    def set_actaea_racemosa_boolean_fields(self):
        """
        Set specific boolean fields for the Actaea racemosa plant profile.
        This function is used to set the boolean fields for the Actaea racemosa plant profile.
        """
        try:
            plant = models.PlantProfile.objects.get(latin_name="Actaea racemosa")
            plant.pollinator_garden = True
            plant.bee_host = True
            plant.hummingbird_friendly = True
            plant.ground_cover = True
            plant.drought_tolerant = True
            plant.salt_tolerant = True
            plant.keystones_species = True
            plant.nitrogen_fixer = True
            plant.germinate_easy = True
            plant.boulevard_garden_tolerant = True
            plant.bird_friendly = True
            plant.hedge = True
            plant.juglone_tolerant = True
            plant.cause_dermatitis = True  # This is false in the CSV file
            plant.produces_burs = True  # This is false in the CSV file
            plant.transplantation_tolerant = True
            plant.limestone_tolerant = True
            plant.school_garden = True
            plant.beginner_friendly = True  # This is false in the CSV file
            plant.moisture_dry = True  # This is false in the CSV file
            plant.moisture_medium = True  # This is false in the CSV file
            plant.moisture_wet = True  # This is true in the CSV file
            plant.full_sun = True  # This is false in the CSV file
            plant.part_shade = True  # This is false in the CSV file
            plant.full_shade = True  # This is true in the CSV file
            plant.spread_by_rhizome = True  # This is false in the CSV file
            plant.dioecious = True  # This is false in the CSV file
            plant.rock_garden = True  # This is false in the CSV file
            plant.septic_tank_safe = True  # This is false in the CSV file
            plant.wetland_garden = True  # This is false in the CSV file
            plant.grasp_candidate = True  # This is false in the CSV file
            plant.acidic_soil_tolerant = True  # This is true in the CSV file
            plant.self_seeding = True  # This is false in the CSV file
            plant.does_not_spread = True  # This is true in the CSV file
            plant.rabbit_tolerant = True  # This is true in the CSV file
            plant.deer_tolerant = True  # This is true in the CSV file
            plant.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully set boolean fields for Actaea racemosa plant profile."
                )
            )
        except models.PlantProfile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("Actaea racemosa plant profile does not exist.")
            )
            raise models.PlantProfile.DoesNotExist(
                "Actaea racemosa plant profile does not exist."
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred while setting boolean fields for Actaea racemosa: {str(e)}"
                )
            )
            raise e
