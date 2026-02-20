from datetime import datetime


def extract_listings() -> list[dict]:
    """
    Simulated extract step.
    Returns dummy listing data.
    """

    return [
        {
            "listing_id": "123",
            "title": "Apto 2 dorm Pocitos",
            "price": 150000,
            "currency": "USD",
            "rooms": 2,
            "baths": 1,
            "size_m2": 70,
            "neighborhood": "Pocitos",
            "scraped_at": datetime.now().isoformat(timespec="seconds"),
        }
    ]