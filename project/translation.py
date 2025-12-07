from modeltranslation.translator import TranslationOptions, translator

from project import models


class BloomColourTranslationOptions(TranslationOptions):
    fields = ("bloom_colour",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class ButterflyTranslationOptions(TranslationOptions):
    fields = ("english_name",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class ConservationStatusTranslationOptions(TranslationOptions):
    fields = ("conservation_status",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class GrowthHabitTranslationOptions(TranslationOptions):
    fields = ("growth_habit",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class HarvestingIndicatorTranslationOptions(TranslationOptions):
    fields = ("harvesting_indicator",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class HarvestingMeanTranslationOptions(TranslationOptions):
    fields = ("harvesting_mean",)  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


class PlantLifespanTranslationOptions(TranslationOptions):
    fields = ("lifespan", "definition")  # Fields to translate
    required_languages = ("fr",)  # Optional: specify required languages


# Cultivar
class CultivarTranslationOptions(TranslationOptions):
    fields = ("one_cultivar",)
    required_languages = ("fr",)


# Ecozone
class EcozoneTranslationOptions(TranslationOptions):
    fields = ("ecozone",)
    required_languages = ("fr",)


# PlantMorphology
class PlantMorphologyTranslationOptions(TranslationOptions):
    fields = ("element",)
    required_languages = ("fr",)


# PackagingMeasure
class PackagingMeasureTranslationOptions(TranslationOptions):
    fields = ("packaging_measure",)
    required_languages = ("fr",)


# SeedEventTable
class SeedEventTableTranslationOptions(TranslationOptions):
    fields = ("seed_event_table",)
    required_languages = ("fr",)


# seedHead
class SeedHeadTranslationOptions(TranslationOptions):
    fields = ("seed_head",)
    required_languages = ("fr",)


# SeedPreparation
class SeedPreparationTranslationOptions(TranslationOptions):
    fields = ("seed_preparation",)
    required_languages = ("fr",)


# SeedStorage
class SeedStorageTranslationOptions(TranslationOptions):
    fields = ("seed_storage",)
    required_languages = ("fr",)


# SeedViabilityTest
class SeedViabilityTestTranslationOptions(TranslationOptions):
    fields = ("seed_viability_test",)
    required_languages = ("fr",)


# SowingDepth
class SowingDepthTranslationOptions(TranslationOptions):
    fields = ("sowing_depth",)
    required_languages = ("fr",)


# ToxicityIndicator
class ToxicityIndicatorTranslationOptions(TranslationOptions):
    fields = ("toxicity_indicator",)
    required_languages = ("fr",)


# Register the models
translator.register(models.BloomColour, BloomColourTranslationOptions)
translator.register(models.ButterflySpecies, ButterflyTranslationOptions)
translator.register(models.ConservationStatus, ConservationStatusTranslationOptions)
translator.register(models.GrowthHabit, GrowthHabitTranslationOptions)
translator.register(models.HarvestingIndicator, HarvestingIndicatorTranslationOptions)
translator.register(models.HarvestingMean, HarvestingMeanTranslationOptions)
translator.register(models.PlantLifespan, PlantLifespanTranslationOptions)
translator.register(models.OneCultivar, CultivarTranslationOptions)
translator.register(models.Ecozone, EcozoneTranslationOptions)
translator.register(models.PlantMorphology, PlantMorphologyTranslationOptions)
translator.register(models.PackagingMeasure, PackagingMeasureTranslationOptions)
translator.register(models.SeedEventTable, SeedEventTableTranslationOptions)
translator.register(models.SeedHead, SeedHeadTranslationOptions)
translator.register(models.SeedPreparation, SeedPreparationTranslationOptions)
translator.register(models.SeedStorage, SeedStorageTranslationOptions)
translator.register(models.SeedViabilityTest, SeedViabilityTestTranslationOptions)
translator.register(models.SowingDepth, SowingDepthTranslationOptions)
translator.register(models.ToxicityIndicator, ToxicityIndicatorTranslationOptions)
