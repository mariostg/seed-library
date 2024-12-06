import pandas as pd
import os, sys
from pathlib import Path
import csv

PWD = os.getenv("PWD")
DATA_DIR = Path(PWD).resolve() / "data"
SOURCE_DIR = DATA_DIR / "source"
OPTION_TABLE_DIR = DATA_DIR / "option_tables"
MAIN_TABLES = DATA_DIR / "main_tables"


def merge_data_files():
    """merge together the All Plants Table with the seed harvesting table"""

    all_plants = pd.read_csv(SOURCE_DIR / "All Plants-Table 1.csv", delimiter=";")
    all_plants = all_plants.fillna("--")

    harvest = pd.read_csv(SOURCE_DIR / "seed_harvesting.csv", delimiter=";")
    harvest = harvest.drop("english_name", axis=1)  # this column exists in native_plants

    merged_file = Path("data/main_tables/native-plants.csv")
    if Path.exists(merged_file):
        print(f"Deleting old {merged_file}")
        Path.unlink(merged_file)
    native_plants = all_plants.merge(harvest, how="left", on="latin_name")
    native_plants.insert(4, "french_name", native_plants.pop("french_name"))
    native_plants.to_csv(merged_file, index=False)


def harvesting_indicators():
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

    df = pd.read_csv(SOURCE_DIR / "seed_harvesting.csv", delimiter=";")
    df = df.fillna("")

    for indicator in indicators:
        csv_file = OPTION_TABLE_DIR / f"harvesting-indicator-{indicator}.csv"
        data_list = list(df[indicator].unique())
        with open(csv_file, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([indicator])
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            for dl in data_list:
                print(dl)
                writer.writerow([dl.strip()])


def _split_bloom_period(df: pd.DataFrame):
    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sept": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
        "": "",
    }
    months_name = months.keys()
    bloom_periods = df.bloom_period.str.replace(",", "").str.replace("?", "").str.split(" ")
    for row_no, period in enumerate(bloom_periods):
        for p in period:
            if p not in months_name:
                raise ValueError(f"Problem in Bloom period. {p} is not recognized at row {row_no}")
    df["bloom_periods"] = bloom_periods
    print(df["bloom_periods"].min())


def native_plants_indicators():
    """Using native plants file created in merge_data_files function, prepare csv
    files for unique values of indicators.  These can then be imported into their
    specific sqlite table to ease"""

    indicators = [
        "category",
        "native",
        "soil",
        "sun_requirement",
        "bloom_period",
        "colour",
    ]
    native_plants = pd.read_csv(SOURCE_DIR / "All Plants-Table 1.csv", delimiter=";")
    native_plants = native_plants.fillna("")
    for indicator in indicators:
        print(f"Working on {indicator}")
        if indicator == "bloom_period":
            _split_bloom_period(native_plants)
        csv_file = OPTION_TABLE_DIR / f"native-plants-{indicator}.csv"
        if Path.exists(csv_file):
            print(f"Deleting old {csv_file}")
            Path.unlink(csv_file)
        data_list = list(sorted(native_plants[indicator].unique()))
        with open(csv_file, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([indicator])
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            for dl in data_list:
                try:
                    writer.writerow([dl.strip()])
                except AttributeError:
                    print(f"Skipped {dl}")


if __name__ == "__main__":
    merge_data_files()
    harvesting_indicators()
    native_plants_indicators()
