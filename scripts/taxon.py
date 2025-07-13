import logging
from pathlib import Path

import pandas as pd

# Create a module-specific logger
logger = logging.getLogger(__name__)


def load_taxon_data(file_path: Path) -> pd.DataFrame:
    """
    Load taxon data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file containing taxon data.

    Returns:
        pd.DataFrame: A DataFrame containing the taxon data.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.suffix == ".csv":
        raise ValueError(f"File is not a CSV file: {file_path}")

    try:
        df = pd.read_csv(file_path, sep="\t", encoding="utf-8")
        # rename column Scientific name to latin_name
        if "Scientific name" in df.columns:
            df.rename(columns={"Scientific name": "latin_name"}, inplace=True)
        else:
            raise ValueError(
                f"Column 'Scientific name' not found in the CSV file: {file_path}"
            )
    except Exception as e:
        logger.exception("Error loading taxon data")
        raise ValueError(f"Error loading taxon data: {e}")


def load_latin_names(file_path: str) -> pd.DataFrame:
    """
    Load Latin names from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file containing Latin names.

    Returns:
        pd.DataFrame: A DataFrame containing the Latin names.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.warning("Error loading Latin names: %s", e)
        return pd.DataFrame()


if __name__ == "__main__":
    # Configure logging
    logger.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Example usage
    data_dir = Path("/Users/mariost-gelais/Documents/datasets/native plants/data/csv")

    latin_names_csv = data_dir / "plant-names-latin - csv.csv"
    latin_names_df = load_latin_names(latin_names_csv)

    taxon_csv = data_dir / "vascan-native-qc-on.csv"
    taxon_df = load_taxon_data(taxon_csv)

    # Merge the two DataFrames on the 'latin_name' column using latin_names_df as the left DataFrame
    merged_df = pd.merge(latin_names_df, taxon_df, on="latin_name", how="left")
    # Keep only the laint_name and url columns
    merged_df = merged_df[["latin_name", "URL"]]
    # given the URL  http://data.canadensys.net/vascan/taxon/8410 pattern match the number at the end
    merged_df["taxon"] = merged_df["URL"].str.extract(r"/(\d+)$")
    # Drop the URL column
    merged_df.drop(columns=["URL"], inplace=True)

    # Save the merged DataFrame to a new CSV file
    output_csv = data_dir / "plant-taxon - csv.csv"
    merged_df.to_csv(output_csv, index=False)
