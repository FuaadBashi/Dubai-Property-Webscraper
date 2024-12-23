from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class PropertyFinderSeleniumScraper:
    BASE_URL = "https://www.propertyfinder.ae"
    service = Service("/Users/fuaad/Downloads/chromedriver")

    def __init__(self, location="Dubai", max_price="150000"):
        self.location = location
        self.max_price = max_price
        self.page_number = 1
        self.property_data = {
            "Property Name": [],
            "Price": [],
            "Area": []
        }
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        options = Options()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        return driver
    
    def open_website(self):
        self.driver.get(self.BASE_URL)
        self.driver.maximize_window()

    def set_search_criteria(self):
        location_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div/form/input")
        property_type_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[1]")
        beds_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[2]')
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[3]')

        location_input.send_keys(self.location)
        property_type_button.click()
        time.sleep(1)
        apartments_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div/button[2]')
        apartments_option.click()

        beds_button.click()
        four_beds_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/ul/li[5]/button')
        time.sleep(1)
        four_beds_option.click()

        search_button.click()

    def set_price_filter(self):
        price_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/button[3]')
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button')

        price_button.click()
        price_input = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[2]/div/div/input')
        price_input.send_keys(self.max_price)

        confirm_button = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/p')
        confirm_button.click()
        time.sleep(1)

        search_button.click()

    def scrape_page_data_first_page(self):
        for i in range(1, 32):
            if i in [6, 7, 13, 19, 20, 26, 28]:
                continue

            try:
                price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text

                self.property_data["Property Name"].append(name)
                self.property_data["Price"].append(price)
                self.property_data["Area"].append(area)
            except NoSuchElementException:
                continue

    def scrape_page_data_other_pages(self):
        for i in range(1, 28):
            if ( i == 6 or i == 19 or i == 19 or i == 28):
                continue

            try:
                price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text

                self.property_data["Property Name"].append(name)
                self.property_data["Price"].append(price)
                self.property_data["Area"].append(area)
            except NoSuchElementException:
                continue

    def navigate_to_next_second_page(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a')
            next_page_url = next_button.get_attribute("href")
            self.driver.get(next_page_url)
        except NoSuchElementException:
            print("No more pages to navigate.")


    def navigate_to_next_page(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a[2]')
            next_page_url = next_button.get_attribute("href")
            self.driver.get(next_page_url)
        except NoSuchElementException:
            print("No more pages to navigate.")

    def run_scraper(self, num_pages=5):
        self.open_website()
        self.set_search_criteria()
        self.set_price_filter()

        for _ in range(num_pages):
            print(f"Scraping page {self.page_number}...")
            if self.page_number == 1:
                self.scrape_page_data_first_page()
                self.page_number += 1
                self.navigate_to_next_second_page()
            else:
                self.scrape_page_data_other_pages()
                self.page_number += 1
                self.navigate_to_next_page()
            
            
        print(self.property_data)
        self.save_to_excel()

    def save_to_excel(self, file_name="properties.xlsx"):
        df = pd.DataFrame(self.property_data)
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = PropertyFinderSeleniumScraper()
    scraper.run_scraper(num_pages=3)
    scraper.close_browser()
