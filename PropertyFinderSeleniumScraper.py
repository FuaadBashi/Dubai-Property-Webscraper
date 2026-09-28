"""Scrapes apartment and villa listings from Property Finder with Selenium.

Drives the site's own search form (location, property type, bedrooms, maximum price), then pages
through the results. Chrome and a matching driver are resolved by Selenium Manager.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from listings import Listing, save, sort_by_price

BASE_URL = "https://www.propertyfinder.ae"

# Search form, as laid out on the site when this was written.
LOCATION_INPUT = "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div/form/input"
LOCATION_BAR = "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div"
FIRST_LOCATION_OPTION = "/html/body/div[6]/div/div/div/button[1]"
SECOND_LOCATION_OPTION = "/html/body/div[6]/div/div/div[2]/button[1]"
PROPERTY_TYPE_BUTTON = "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[1]"
BEDS_BUTTON = "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[2]"
SEARCH_BUTTON = "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[3]"
PRICE_BUTTON = "/html/body/div[1]/div/div[3]/div/div[2]/button[3]"
PRICE_INPUT = "/html/body/div[7]/div/div[1]/div[2]/div/div/input"
PRICE_CONFIRM = "/html/body/div[7]/div/div[2]/p"
FILTER_SEARCH_BUTTON = "/html/body/div[1]/div/div[3]/div/button"

# Results. Fields are read relative to each <li>, so ad slots (which have no <article>) are skipped
# by their shape rather than by a hard-coded list of positions that drifted between pages.
RESULT_ITEMS = "/html/body/div[1]/div/main/div[5]/div[1]/ul/li"
ITEM_PRICE = "./article/div/div/section[2]/div[1]/div[1]/div/p"
ITEM_NAME = "./article/div/div/section[2]/div[2]/div[1]/p"
ITEM_AREA = "./article/div/div/section[2]/div[2]/div[2]/p[3]"
ITEM_LINK = "./article/a"
NEXT_PAGE_FROM_FIRST = "/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a"
NEXT_PAGE_FROM_LATER = "/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a[2]"


@dataclass(frozen=True)
class Search:
    label: str
    type_option: str
    beds_option: str
    max_price: str
    output: str


SEARCHES = {
    "apartments": Search(
        "apartments",
        type_option="/html/body/div[6]/div/div/button[2]",
        beds_option="/html/body/div[6]/div/div[1]/ul/li[5]/button",  # 4 beds
        max_price="150000",
        output="apartment-properties.xlsx",
    ),
    "villas": Search(
        "villas",
        type_option="/html/body/div[6]/div/div/button[3]",
        beds_option="/html/body/div[6]/div/div[1]/ul/li[6]/button",  # 5 beds
        max_price="200000",
        output="villa-properties.xlsx",
    ),
}
LOCATIONS = ("dubai", "sharjah")


class PropertyFinderScraper:
    def __init__(self, headless: bool = False, pause: float = 1.0):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        # No hard-coded chromedriver path: the old one only existed on the author's machine.
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.pause_seconds = pause

    def pause(self, factor: float = 1.0) -> None:
        """The site animates its dropdowns, so each step waits for the UI to settle."""
        time.sleep(self.pause_seconds * factor)

    def click(self, xpath: str) -> None:
        self.driver.find_element(By.XPATH, xpath).click()

    def search(self, search: Search) -> None:
        self.driver.get(BASE_URL)
        self.driver.maximize_window()

        for i, location in enumerate(LOCATIONS):
            if i > 0:
                self.click(LOCATION_BAR)
                self.pause(3)
            field = self.driver.find_element(By.XPATH, LOCATION_INPUT)
            field.click()
            field.send_keys(location)
            self.pause(5)
            self.click(FIRST_LOCATION_OPTION if i == 0 else SECOND_LOCATION_OPTION)
            self.pause(5)

        self.click(PROPERTY_TYPE_BUTTON)
        self.pause()
        self.click(search.type_option)
        self.click(BEDS_BUTTON)
        self.pause(3)
        self.click(search.beds_option)
        self.pause()
        self.click(SEARCH_BUTTON)

        self.click(PRICE_BUTTON)
        self.pause(2)
        self.driver.find_element(By.XPATH, PRICE_INPUT).send_keys(search.max_price)
        self.click(PRICE_CONFIRM)
        self.pause()
        self.click(FILTER_SEARCH_BUTTON)

    def scrape_page(self) -> list[Listing]:
        listings = []
        for item in self.driver.find_elements(By.XPATH, RESULT_ITEMS):
            try:
                listings.append(
                    Listing(
                        name=item.find_element(By.XPATH, ITEM_NAME).text,
                        price=item.find_element(By.XPATH, ITEM_PRICE).text,
                        area=item.find_element(By.XPATH, ITEM_AREA).text,
                        link=item.find_element(By.XPATH, ITEM_LINK).get_attribute("href"),
                    )
                )
            except NoSuchElementException:
                continue  # an ad or promoted tile
        return listings

    def next_page(self, current: int) -> bool:
        xpath = NEXT_PAGE_FROM_FIRST if current == 1 else NEXT_PAGE_FROM_LATER
        try:
            url = self.driver.find_element(By.XPATH, xpath).get_attribute("href")
        except NoSuchElementException:
            return False
        self.driver.get(url)
        return True

    def run(self, search: Search, pages: int) -> list[Listing]:
        self.search(search)
        listings: list[Listing] = []
        for page in range(1, pages + 1):
            print(f"Scraping {search.label}, page {page}...")
            listings += self.scrape_page()
            if page < pages and not self.next_page(page):
                print("No more pages.")
                break
        return sort_by_price(listings)

    def close(self) -> None:
        self.driver.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", choices=[*SEARCHES, "both"], default="both")
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    for key in SEARCHES if args.type == "both" else [args.type]:
        search = SEARCHES[key]
        scraper = PropertyFinderScraper(headless=args.headless)
        try:
            listings = scraper.run(search, args.pages)
        finally:
            scraper.close()
        path = save(listings, args.out_dir / search.output)
        print(f"Saved {len(listings)} {search.label} to {path}")


if __name__ == "__main__":
    main()
