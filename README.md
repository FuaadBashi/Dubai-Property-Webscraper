# Dubai Property Scraping Experiments

Two Python approaches to collecting property listings: direct HTML parsing with Requests/BeautifulSoup and browser automation with Selenium.

## Setup

Use Python 3 and a local Chrome installation for the Selenium script.

```bash
git clone https://github.com/FuaadBashi/Dubai-Property-Webscraper.git
cd Dubai-Property-Webscraper
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4 selenium pandas openpyxl
```

## Run an experiment

```bash
python BayutBeautifulSoupScraper.py
# Or run the browser-based Property Finder workflow:
python PropertyFinderSeleniumScraper.py
```

Review the URL, headers, search criteria, and output paths in the selected script first. The source contains site-specific selectors and browser assumptions; website changes can require updates.

## Code to explore

- [BayutBeautifulSoupScraper.py](BayutBeautifulSoupScraper.py): request, parse, and display stages.
- [PropertyFinderSeleniumScraper.py](PropertyFinderSeleniumScraper.py): browser interaction, filters, pagination, and spreadsheet export.

The checked-in spreadsheets are historical outputs, not live market data. This repository demonstrates extraction techniques and does not claim current coverage or listing accuracy. Use only sources you are permitted to access.
