"""Shared listing type, price parsing, sorting and export for both scrapers."""

from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path


@dataclass(frozen=True)
class Listing:
    name: str
    price: str
    area: str
    link: str = ""

    @property
    def price_value(self) -> int | None:
        return parse_price(self.price)


def parse_price(text: str) -> int | None:
    """Extracts the number from a price such as "150,000 AED/year"; None if there isn't one.

    The original parsed int(text.split(" ")[0]), which crashed the whole run on "Ask for price".
    """
    match = re.search(r"\d[\d,]*", text)
    return int(match.group().replace(",", "")) if match else None


def sort_by_price(listings: list[Listing]) -> list[Listing]:
    """Cheapest first; listings without a price go last."""
    return sorted(listings, key=lambda item: (item.price_value is None, item.price_value or 0))


COLUMNS = {"name": "Property Name", "price": "Price", "area": "Area", "link": "Link"}


def save(listings: list[Listing], path: Path) -> Path:
    """Writes .csv, or .xlsx when the name ends in .xlsx (needs pandas and openpyxl)."""
    rows = [{COLUMNS[k]: v for k, v in asdict(listing).items()} for listing in listings]
    headers = [COLUMNS[f.name] for f in fields(Listing)]
    if path.suffix.lower() == ".xlsx":
        import pandas as pd

        pd.DataFrame(rows, columns=headers).to_excel(path, index=False)
    else:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    return path
