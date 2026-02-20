from src.extract import extract_listings


def main() -> None:
    listings = extract_listings()

    print("Extracted listings:")
    for item in listings:
        print(item)


if __name__ == "__main__":
    main()