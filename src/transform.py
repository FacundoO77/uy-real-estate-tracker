import re
from datetime import datetime

def parse_price(price_raw: str | None) -> tuple[int | None, str | None]:
    """
    Parse raw price string into numeric price and normalized currency.
    """
    if not price_raw:
        return None, None

    price_raw = price_raw.strip()

    currency = None
    if "$" in price_raw:
        currency = "UYU"
    elif "US$" in price_raw or "USD" in price_raw:
        currency = "USD"

    digits = re.sub(r"[^\d]", "", price_raw)
    price = int(digits) if digits else None

    return price, currency

def format_datetime(dt_str: str | None) -> str | None:
    if not dt_str:
        return None

    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return dt_str
    
def parse_size(size_raw: str | None) -> int | None:
    """
    Parse raw size string like '71 m²' into integer.
    """
    if not size_raw:
        return None

    digits = re.sub(r"[^\d]", "", size_raw)
    return int(digits) if digits else None

def clean_text(value: str | None) -> str | None:
    """
    Strip and normalize text fields.
    """
    if not value:
        return None

    value = value.strip()
    return value if value else None

def transform_listing(raw_listing: dict) -> dict:
    price, currency = parse_price(raw_listing.get("price_raw"))
    size_m2 = parse_size(raw_listing.get("size_m2_raw"))

    return {
        "title": clean_text(raw_listing.get("title_raw")),
        "owner": clean_text(raw_listing.get("owner_raw")),
        "listing_id": raw_listing.get("listing_id_raw"),
        "listing_url": raw_listing.get("listing_url"),
        "price": price,
        "currency": currency,
        "rooms": raw_listing.get("rooms_filter"),
        "baths": raw_listing.get("baths_filter"),
        "size_m2": size_m2,
        "neighborhood": clean_text(raw_listing.get("neighborhood_raw")),
        "source_url": raw_listing.get("source_url"),
        "scraped_at": format_datetime(raw_listing.get("scraped_at")),
    }

def transform_listings(raw_listings: list[dict]) -> list[dict]:
    """
    Transform a list of raw listings into clean listings.
    """
    return [transform_listing(listing) for listing in raw_listings]