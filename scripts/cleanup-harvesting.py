import pandas as pd
import os, sys
from pathlib import Path
import csv

PWD = os.getenv("PWD")
DATA_DIR = Path(PWD).resolve() / "data"
SOURCE_DIR = DATA_DIR / "source"
OPTION_TABLE_DIR = DATA_DIR / "option_tables"
MAIN_TABLES = DATA_DIR / "main_tables"
plants = pd.read_csv(SOURCE_DIR / "All Plants-Table 1.csv", delimiter=";")
harvest = pd.read_csv(SOURCE_DIR / "seed_harvesting.csv", delimiter=";")
df = harvest.merge(plants, on="latin_name", how="left").fillna("NA")
df.to_csv(MAIN_TABLES / "full-list.csv")

indicators = [
    "harvesting_indicator",
    "harvesting_mean",
    "latin_name",
    "one_cultivar",
    "packaging_measure",
    "seed_head",
    "seed_storage",
    "sharing_priority",
    "viability_test",
    "seed_storage",
]
for indicator in indicators:
    csv_file = OPTION_TABLE_DIR / f"{indicator}.csv"
    data_list = list(df[indicator].unique())
    with open(csv_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([indicator])
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        for dl in data_list:
            writer.writerow([dl.strip()])
