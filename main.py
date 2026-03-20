from src.extract import extract_listings
from src.transform import transform_listings
from src.load import save_raw_csv, save_clean_csv
from src.utils import validate_volume, validate_duplicates, validate_nulls

RAW_OUTPUT_PATH = "export/raw_listings.csv"
CLEAN_OUTPUT_PATH = "export/clean_listings.csv"


def run_pipeline():
    try:
        print("Starting pipeline...")

        # 1. Extract
        raw_listings = extract_listings()
        print(f"Extracted {len(raw_listings)} raw listings")

        if not raw_listings:
            print("No raw listings extracted. Stopping pipeline.")
            return

        # 2. Save raw
        save_raw_csv(raw_listings, RAW_OUTPUT_PATH)

        # 3. Transform
        clean_listings = transform_listings(raw_listings)
        print(f"Transformed {len(clean_listings)} listings")

        # 4. Validate before the data cleaning
        validate_volume(clean_listings)
        validate_duplicates(clean_listings)
        validate_nulls(clean_listings)

        # 5. Save clean
        save_clean_csv(clean_listings, CLEAN_OUTPUT_PATH)

        print("Pipeline finished.")

    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()