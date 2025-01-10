"""
Just a file to experiment with code as needed
"""

import os
import sys
from pathlib import Path

import django
import pandas as pd

PWD = os.getenv("PWD")
BASE_DIR = Path(PWD).resolve()
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from project.models import Habit, PlantProfile

# latin_name,english_name,french_name,url,light_from,light_to,bloom_start,bloom_end,soil_humidity_min,soil_humidity_max,min_height,max_height,size,stratification_detail,stratification_duration,sowing_depth,sowing_period,sharing_priority,harvesting_start,harvesting_end,harvesting_indicator,harvesting_mean,seed_head,remove_non_seed_material,viability_test,seed_storage,one_cultivar,packaging_measure,dormancy,seed_preparation,hyperlink,envelope_label_link,harvesting_video_link,seed_picture_link,pods_seed_head_picture_link
# url = "http://data.canadensys.net/vascan/api/0.1/search.json?q=Actaea%20racemosa"


def taxon_habit_to_csv():
    """Read vascan data and merge with plant profiles to get taxon and habit"""
    df_vascan = pd.read_csv("/Users/mariost-gelais/Documents/datasets/native plants/vascan-native-qc-on.csv", sep="\t")

    plants = PlantProfile.objects.all()
    df_plants = pd.DataFrame(list(plants.values()))

    df_merged = pd.merge(
        df_plants,
        df_vascan,
        how="left",
        left_on="latin_name",
        right_on=df_vascan["Scientific name"].str.lower(),
    )
    # columns = ["Scientific name", "latin_name", "english_name", "french_name", "Habit", "URL"]
    columns = ["Scientific name", "latin_name", "english_name", "french_name", "Habit", "taxon"]
    df_merged["taxon"] = df_merged.URL.str.split("/", expand=True)[5]
    final_df = df_merged[columns]
    final_df.to_csv(
        "/Users/mariost-gelais/Documents/datasets/native plants/vascan-native-taxon.csv",
        sep="\t",
        index=False,
    )


def taxon_to_db():
    """Read vascan taxon data and update plant profiles"""
    df_vascan = pd.read_csv("/Users/mariost-gelais/Documents/datasets/native plants/vascan-native-taxon.csv", sep="\t")
    df_vascan["taxon"] = df_vascan["taxon"].astype("string").str.split(".").str[0]
    for _, row in df_vascan.iterrows():
        plant = PlantProfile.objects.get(latin_name=row["latin_name"])
        plant.taxon = row["taxon"]
        plant.save()


def habit_to_db():
    """Read vascan habit data and update plant profiles"""
    df_vascan = pd.read_csv("/Users/mariost-gelais/Documents/datasets/native plants/vascan-native-taxon.csv", sep="\t")
    for _, row in df_vascan.iterrows():
        plant = PlantProfile.objects.get(latin_name=row["latin_name"])
        try:
            habit = Habit.objects.get(habit=row["Habit"])
            plant.habit = habit
            plant.save()
        except Habit.DoesNotExist:
            pass


def inaturalist_taxon_to_db():
    """Read inaturalist data and update plant profiles"""
    df_inaturalist = pd.read_csv(
        "/Users/mariost-gelais/Documents/datasets/native plants/seed-library-with-inat-taxon.csv", sep="\t"
    )
    df_inaturalist["inat_taxon"] = df_inaturalist["inat_taxon"].astype("string").str.split(".").str[0]
    for _, row in df_inaturalist.iterrows():
        plant = PlantProfile.objects.get(latin_name=row["latin_name"].lower())
        plant.inaturalist_taxon = row["inat_taxon"]
        plant.save()


if __name__ == "__main__":
    inaturalist_taxon_to_db()
    # habit_to_db()
    # taxon_to_db()
    # taxon_to_csv()
