def validate_volume(data):
    print(f"Listings: {len(data)}")

    if len(data) < 200:
        print("⚠️ Warning: too few listings")


def validate_duplicates(data):
    ids = [d.get("listing_id") for d in data]
    duplicates = len(ids) - len(set(ids))

    print(f"Duplicates: {duplicates}")


def validate_nulls(data):
    null_price = sum(1 for d in data if d.get("price") is None)
    null_id = sum(1 for d in data if d.get("listing_id") is None)

    print(f"Null prices: {null_price}")
    print(f"Null ids: {null_id}")