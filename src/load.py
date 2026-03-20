import pandas as pd

RAW_COLUMNS = [
    "title_raw",
    "owner_raw",
    "listing_id_raw",
    "listing_url",
    "price_raw",
    "currency_raw",
    "rooms_filter",
    "baths_filter",
    "size_m2_raw",
    "neighborhood_raw",
    "source_url",
    "scraped_at",
]

CLEAN_COLUMNS = [
    "title",
    "owner",
    "listing_id",
    "listing_url",
    "price",
    "currency",
    "rooms",
    "baths",
    "size_m2",
    "neighborhood",
    "source_url",
    "scraped_at",
]


def save_raw_csv(data: list[dict], path: str):
    df = pd.DataFrame(data)
    df = df.reindex(columns=RAW_COLUMNS)
    df.to_csv(path, index=False, encoding="utf-8-sig", sep=";")


def save_clean_csv(data: list[dict], path: str):
    df = pd.DataFrame(data)
    df = df.reindex(columns=CLEAN_COLUMNS)
    df.to_csv(path, index=False, encoding="utf-8-sig", sep=";")