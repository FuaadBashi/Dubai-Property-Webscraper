from pathlib import Path

import pytest

from BayutBeautifulSoupScraper import parse_listings
from listings import Listing, parse_price, save, sort_by_price

CARD = """
<li class="a37d52f0">
  <a href="/property/details-{id}.html"></a>
  <span class="dc381b54">{price}</span>
  <h2 class="_948d9e0a _371e9918">{name}</h2>
  <span class="_19e94678 f8d4dd58">{area}</span>
</li>
"""


def page(*cards: str) -> str:
    return "<html><body><ul>" + "".join(cards) + "</ul></body></html>"


def test_each_card_yields_exactly_one_listing_with_its_own_fields():
    html = page(
        CARD.format(id=1, price="95,000", name="Marina studio", area="450 sqft"),
        CARD.format(id=2, price="180,000", name="Downtown 2BR", area="1,200 sqft"),
        CARD.format(id=3, price="72,000", name="JVC 1BR", area="700 sqft"),
    )

    listings = parse_listings(html)

    # The original collected every field once per card: 9 names for 3 cards.
    assert [item.name for item in listings] == ["Marina studio", "Downtown 2BR", "JVC 1BR"]
    assert listings[1] == Listing(
        "Downtown 2BR", "180,000", "1,200 sqft", "/property/details-2.html"
    )


def test_cards_without_a_price_or_title_are_skipped():
    ad = '<li class="a37d52f0"><div>Sponsored</div></li>'
    html = page(ad, CARD.format(id=1, price="95,000", name="Marina studio", area="450 sqft"))

    assert [item.name for item in parse_listings(html)] == ["Marina studio"]


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("150,000 AED/year", 150000),
        ("AED 95,500", 95500),
        ("72000", 72000),
        ("Ask for price", None),
    ],
)
def test_prices_are_parsed_from_their_display_text(text, value):
    assert parse_price(text) == value


def test_sorting_puts_the_cheapest_first_and_unpriced_last():
    items = [
        Listing("B", "200,000 AED", ""),
        Listing("C", "Ask for price", ""),
        Listing("A", "90,000 AED", ""),
    ]

    assert [item.name for item in sort_by_price(items)] == ["A", "B", "C"]


def test_listings_save_to_csv(tmp_path: Path):
    path = save([Listing("Marina studio", "95,000", "450 sqft", "/x")], tmp_path / "out.csv")

    assert path.read_text().splitlines() == [
        "Property Name,Price,Area,Link",
        'Marina studio,"95,000",450 sqft,/x',
    ]
