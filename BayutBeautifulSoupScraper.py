import smtplib
import requests
from bs4 import BeautifulSoup

class BayutBeautifulSoupScraper:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.property_data = {
            "name": [],
            "price": [],
            "area": []
        }

    def fetch_page(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")
            return None

    def extract_data(self, soup):
        if soup is None:
            print("No soup object to parse.")
            return

        try:
            for listing in soup.find_all(class_="a37d52f0"):
                for price in soup.find_all(class_="dc381b54"):
                    self.property_data["price"].append(price.text)

                for property_name in soup.find_all(class_="_948d9e0a _371e9918"):
                    self.property_data["name"].append(property_name.text)

                for size in soup.find_all(class_="_19e94678 f8d4dd58"):
                    self.property_data["area"].append(size.text)

        except Exception as e:
            print(f"An error occurred while extracting data: {e}")

    def display_data(self):
        for name, price, area in zip(self.property_data["name"], self.property_data["price"], self.property_data["area"]):
            print(f"Property Name: {name}, Price: {price} AED per month, Area: {area}")

    def run(self):
        soup = self.fetch_page()
        self.extract_data(soup)
        self.display_data()

if __name__ == "__main__":
    URL = "https://www.bayut.com/to-rent/property/dubai/?ipckg=true&rent_frequency=any&utm_source=google&utm_medium=cpc&utm_campaign=%7Bcampaignname%7D&gclid=CjwKCAiA65m7BhAwEiwAAgu4JGU5idzaYqbPVmXinDPZ7aI4cE64664Wq6IHqNVTce1xHj0Tfwie-RoCArUQAvD_BwE"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    scraper = BayutBeautifulSoupScraper(URL, HEADERS)
    scraper.run()
