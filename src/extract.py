import requests
import lxml.html
import re
from datetime import datetime
from pprint import pprint

BASE_URL = "https://www.infocasas.com.uy/alquiler/inmuebles/montevideo/2-dormitorios/1-bano"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def build_search_url(page: int) -> str:
    """
    Build the correct search URL depending on page.
    """

    if page == 1:
        return BASE_URL

    return f"{BASE_URL}/pagina{page}"


def fetch_page(url: str) -> str:
    """
    Download HTML content.
    """

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    print(response.status_code)
    return response.text


def parse_listings(html: str) -> list[dict]:
    """
    Parse property cards using XPath.
    """

    tree = lxml.html.fromstring(html)

    listings = []

    # ESTE XPATH LO VAS A AJUSTAR
    cards = tree.xpath("//section[@class='listingsWrapper']/div[1]")

    for card in cards:

        try:

            title = card.xpath(".//div/h2[contains(@class,'lc-title body')]/text()")
            owner = card.xpath(".//div[@class='lc-owner-name']/text()")
            price = card.xpath(".//div[@class='property-price-tag']/p[@class='main-price']/text()")
            location = card.xpath(".//*[contains(@class,'location')]/text()")
            link = card.xpath(".//a/@href")

            title = title[0].strip() if title else None
            owner = owner[0].strip() if owner else None
            price = price[0].strip() if price else None
            location = location[1].strip() if location else None

            url = None
            if link:
                url = "https://www.infocasas.com.uy" + link[0]
                match = re.search(r"(\d+)$", url)
                clean_id = match.group(1) if match else None

            listing = {
                "title": title,
                "owner": owner,
                "listing_id": clean_id,
                "listing_url": url,
                "price": price,
                "currency": price[0],
                "rooms": 2,
                "baths": 1,
                "size_m2": None,
                "neighborhood": location,
                "url": BASE_URL,
                "scraped_at": datetime.now().isoformat(timespec="seconds"),
            }

            listings.append(listing)
            #print(listings)
        except Exception as e:

            pprint("Error parsing listing:", e)

    return listings


def extract_listings(pages: int = 1) -> list[dict]:
    """
    Extract listings from InfoCasas.
    """

    all_listings = []

    for page in range(1, pages + 1):

        url = build_search_url(page)

        print(f"Scraping page: {url}")

        html = fetch_page(url)

        listings = parse_listings(html)

        all_listings.extend(listings)

    return all_listings


if __name__ == "__main__":

    listings = extract_listings(pages=1)

    print(f"Extracted {len(listings)} listings")

    for listing in listings[:5]:
        pprint(listing)