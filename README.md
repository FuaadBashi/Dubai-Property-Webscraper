# Dubai Property Scrapers

[![CI](https://github.com/FuaadBashi/Dubai-Property-Webscraper/actions/workflows/ci.yml/badge.svg)](https://github.com/FuaadBashi/Dubai-Property-Webscraper/actions/workflows/ci.yml)

Two approaches to collecting UAE rental listings, side by side:

| Script | Site | Technique | Output |
| --- | --- | --- | --- |
| [`BayutBeautifulSoupScraper.py`](BayutBeautifulSoupScraper.py) | Bayut | Requests + BeautifulSoup: fetch server-rendered HTML and parse listing cards | console, CSV or Excel |
| [`PropertyFinderSeleniumScraper.py`](PropertyFinderSeleniumScraper.py) | Property Finder | Selenium: drive the site's search form (locations, type, bedrooms, max price) and paginate | Excel |

Both produce the same `Listing` records (name, price, area, link), sorted cheapest first. Sample
output from a real run (58 apartments, 63 villas in Dubai and Sharjah) is in
[`sample-output/`](sample-output).

## Highlights

- **Per-card parsing.** Each field is read from inside its own listing card, and ads without a
  price or title are skipped.
- **Shared, tested core.** `listings.py` holds the `Listing` dataclass, price parsing
  (`"150,000 AED/year"` → `150000`, with `"Ask for price"` handled), sorting and CSV/Excel export.
  Parsing is tested against fixture HTML, so the tests need no network.
- **Configured searches.** Apartment and villa searches are `Search` dataclasses with their own
  filters and output file, run by one code path.
- **Selectors in one place.** Every XPath and class name is a named constant at the top of its
  script. When the site's markup changes, the fix is a single edit.

## Getting started

Requires Python 3.10+. The Selenium scraper also needs Google Chrome; Selenium Manager fetches a
matching driver automatically.

```bash
git clone https://github.com/FuaadBashi/Dubai-Property-Webscraper.git
cd Dubai-Property-Webscraper
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python BayutBeautifulSoupScraper.py --out listings.csv
python PropertyFinderSeleniumScraper.py --type apartments --pages 3 --headless
```

Both sites change their markup from time to time. If a scraper finds nothing, update the
selector constants at the top of the script. Check each site's terms of use before scraping, and
keep request volumes modest.

## Tests

```bash
pip install pytest ruff requests beautifulsoup4
pytest
ruff format --check . && ruff check .
```
