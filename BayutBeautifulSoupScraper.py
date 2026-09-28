"""Scrapes rental listings from a Bayut search results page with Requests and BeautifulSoup."""

from __future__ import annotations

import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from listings import Listing, save, sort_by_price

DEFAULT_URL = "https://www.bayut.com/to-rent/property/dubai/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

# Bayut's generated class names; update these if the site's markup changes.
LISTING_CARD = "a37d52f0"
PRICE = "dc381b54"
NAME = "_948d9e0a _371e9918"
AREA = "_19e94678 f8d4dd58"


def fetch(url: str, timeout: float = 20) -> str:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_listings(html: str) -> list[Listing]:
    """One Listing per card, reading each field from inside that card.

    The original searched the whole page for every field once per card, so each price, name and
    area was collected N times for N cards.
    """
    soup = BeautifulSoup(html, "html.parser")
    listings = []
    for card in soup.find_all(class_=LISTING_CARD):
        price, name, area = (card.find(class_=cls) for cls in (PRICE, NAME, AREA))
        if price is None or name is None:
            continue  # ad slots and promoted tiles have no price or title
        link = card.find("a", href=True)
        listings.append(
            Listing(
                name=name.get_text(strip=True),
                price=price.get_text(strip=True),
                area=area.get_text(strip=True) if area else "",
                link=link["href"] if link else "",
            )
        )
    return listings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="a Bayut search results URL")
    parser.add_argument("--out", type=Path, help="save to .csv or .xlsx")
    args = parser.parse_args()

    try:
        listings = sort_by_price(parse_listings(fetch(args.url)))
    except requests.RequestException as e:
        raise SystemExit(f"Could not fetch {args.url}: {e}") from None

    for item in listings:
        print(f"{item.name} | {item.price} AED | {item.area}")
    print(f"{len(listings)} listings")
    if args.out:
        print(f"Saved to {save(listings, args.out)}")


if __name__ == "__main__":
    main()
