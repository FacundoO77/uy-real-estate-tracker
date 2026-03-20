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


def fetch_page(url: str) -> tuple[str, str]:
    """
    Download HTML content and return html + final response URL.
    """
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    print(response.status_code)
    return response.text, response.url


def parse_listings(html: str, source_url: str, source_page: int) -> list[dict]:
    """
    Parse property cards using XPath.
    """

    tree = lxml.html.fromstring(html)

    listings = []

    # ESTE XPATH LO VAS A AJUSTAR
    cards = tree.xpath("//section[@class='listingsWrapper']/div")

    for card in cards:

        try:

            title = card.xpath(".//div/h2[contains(@class,'lc-title body')]/text()")
            owner = card.xpath(".//div[@class='lc-owner-name']/text()")
            price = card.xpath(".//div[@class='property-price-tag']/p[@class='main-price']/text()")
            location = card.xpath(".//*[contains(@class,'location')]/text()")
            link = card.xpath(".//a/@href") #//div[contains(@class,"typologyTag")]/span[3]/strong
            size_m2 = card.xpath(".//div[contains(@class,'typologyTag')]/span[3]/strong/text()") 

            title = title[0].strip() if title else None
            owner = owner[0].strip() if owner else None
            price = price[0].strip() if price else None
            location = location[1].strip() if location else None
            size_m2 = size_m2[0].strip() if size_m2 else None 
            

            url = None
            clean_id = None

            if link:
                url = "https://www.infocasas.com.uy" + link[0]
                match = re.search(r"(\d+)$", url)
                clean_id = match.group(1) if match else None

            listing = {
                "title_raw": title,
                "owner_raw": owner,
                "listing_id_raw": clean_id,
                "listing_url": url,
                "price_raw": price,
                "currency_raw": price[0] if price else None,
                "rooms_filter": 2,
                "baths_filter": 1,
                "size_m2_raw": size_m2,
                "neighborhood_raw": location,
                "source_url": source_url,
                "source_page": source_page,
                "scraped_at": datetime.now().isoformat(timespec="seconds"),
            }

            listings.append(listing)
            #print(listings)
        except Exception as e:

            pprint("Error parsing listing:", e)

    return listings

#Extracts the maximum number of pages from the html in order to use it later as a limiter .
def get_max_pages(html: str) -> int:
    tree = lxml.html.fromstring(html)

    pages = tree.xpath("//ul[@aria-label='Pagination']/li/a/text()")

    # limpiar solo números
    pages = [p.strip() for p in pages if p.strip().isdigit()]

    if not pages:
        return 1

    return max(map(int, pages))

def extract_listings() -> list[dict]:
    all_listings = []

    first_url = build_search_url(1)
    html, final_url = fetch_page(first_url)

    max_pages = get_max_pages(html)
    max_pages_debug = min(max_pages, 15)

    print(f"Detected max pages: {max_pages}")

    for page in range(1, max_pages_debug + 1):
        url = build_search_url(page)
        print(f"Scraping page: {url}")

        try:
            html, final_url = fetch_page(url)

            listings = parse_listings(
                html,
                source_url=url,
                source_page= final_url,
            )

            if not listings:
                print(f"No listings found on page {page}. Stopping.")
                break

            all_listings.extend(listings)

        except Exception as e:
            pprint(f"Error scraping page {page}: {e}")
            break

    return all_listings

if __name__ == "__main__":

    listings = extract_listings()

    print(f"Extracted {len(listings)} listings")

    #for listing in listings[:5]: # USED FOR DEBUGGING
    #    pprint(listing)