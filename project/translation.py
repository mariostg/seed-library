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


# Register the models
translator.register(models.BloomColour, BloomColourTranslationOptions)
translator.register(models.ButterflySpecies, ButterflyTranslationOptions)
translator.register(models.ConservationStatus, ConservationStatusTranslationOptions)
translator.register(models.GrowthHabit, GrowthHabitTranslationOptions)
translator.register(models.HarvestingIndicator, HarvestingIndicatorTranslationOptions)
translator.register(models.HarvestingMean, HarvestingMeanTranslationOptions)
