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

    def __init__(self, location="Dubai"):
        self.location = location
        
        self.apartment_price = '150000'
        self.villa_price = '200000'
        self.page_number = 1
        self.apartment_data = {
            "Property Name": [],
            "Price": [],
            "Area": [], 
            "Link": [], 
        }
        self.temp_apartment_data = {
            "Property Name": [],
            "Price": [],
            "Area": [], 
            "Link": [], 
        }
        self.villa_data = {
            "Property Name": [],
            "Price": [],
            "Area": [], 
            "Link": [], 
        }
        self.temp_villa_data = {
            "Property Name": [],
            "Price": [],
            "Area": [], 
            "Link": [], 
        }
        self.images = []
        self.driver = self._initialize_driver()
        self.searching_is_apartments = True

    def _initialize_driver(self):
        options = Options()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        return driver
    
    def open_website(self):
        self.driver.get(self.BASE_URL)
        self.driver.maximize_window()

    def set_search_apartment_criteria(self):
        location_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div/form/input")
        property_type_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[1]")
        beds_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[2]')
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[3]')

        location_input.send_keys(self.location)
        property_type_button.click()
        time.sleep(1)
        apartments_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div/button[2]')
        time.sleep(2)
        apartments_option.click()

        beds_button.click()
        four_beds_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/ul/li[5]/button')
        time.sleep(1)
        four_beds_option.click()
        time.sleep(1)
        search_button.click()
    
    def set_search_villa_criteria(self):
        location_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div/form/input")
        property_type_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[1]")
        beds_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[2]')
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[3]')

        location_input.send_keys(self.location)
        property_type_button.click()
        time.sleep(1)
        villa_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div/button[3]')

                                                        
        time.sleep(1)
        villa_option.click()

        beds_button.click()
        time.sleep(1)
        five_beds_option = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/ul/li[6]/button')
        # /html/body/div[4]/div/div[1]/ul/li[6]/button
        time.sleep(1)
        five_beds_option.click()
        time.sleep(1)
        search_button.click()

    def set_price_filter(self):
        price_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/button[3]')
        
        search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button')

        price_button.click()

        
        if (self.searching_is_apartments == True):
            price_input = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[2]/div/div/input')
            price_input.send_keys(self.apartment_price)
            confirm_button = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/p')
            confirm_button.click()
            time.sleep(1)
            search_button.click()
        else:    
            price_input = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[2]/div/div/input')
            price_input.send_keys(self.villa_price)
            confirm_button = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/p')
            time.sleep(1)
            confirm_button.click()
            time.sleep(1)
            search_button.click()
        

    def scrape_page_data_first_page(self):
        if (self.searching_is_apartments == True):
            for i in range(1, 32):
                if i in [6, 7, 13, 19, 20, 26, 28]:
                    continue

                try:
                    price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                    name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                    area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text
                    link = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/a')
                    link = link.get_attribute("href")
                    # image =  self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[1]/div/div[2]/div[1]/a/div/img[2]')
                                                        

                    self.apartment_data["Property Name"].append(name)
                    self.apartment_data["Price"].append(price)
                    self.apartment_data["Area"].append(area)
                    self.apartment_data["Link"].append(link)
                    # self.images.append(image)
                except NoSuchElementException:
                    continue
        else:
            for i in range(1, 32):
                if i in [6, 7, 13, 19, 20, 26, 28]:
                    continue

                try:
                    price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                    name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                    area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text
                    link = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/a')
                    link = link.get_attribute("href")
                    # image =  self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[1]/div/div[2]/div[1]/a/div/img[2]')
                                                        

                    self.villa_data["Property Name"].append(name)
                    self.villa_data["Price"].append(price)
                    self.villa_data["Area"].append(area)
                    self.villa_data["Link"].append(link)
                    # self.images.append(image)
                except NoSuchElementException:
                    continue

    def scrape_page_data_other_pages(self):
        if (self.searching_is_apartments == True):
            for i in range(1, 28):
                if ( i == 6 or i == 19 or i == 19 or i == 28):
                    continue

                try:
                    price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                    name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                    area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text
                    link = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/a')
                    link = link.get_attribute("href")
                    # image =  self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[1]/div/div[2]/div[1]/a/div/img[2]')

                    self.apartment_data["Property Name"].append(name)
                    self.apartment_data["Price"].append(price)
                    self.apartment_data["Area"].append(area)
                    self.apartment_data["Link"].append(link)
                    # self.images.append(image)
                except NoSuchElementException:
                    continue
        else:
            for i in range(1, 28):
                if ( i == 6 or i == 19 or i == 19 or i == 28):
                    continue

                try:
                    price = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p').text
                    name = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p').text
                    area = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]').text
                    link = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/a')
                    link = link.get_attribute("href")
                    # image =  self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[1]/div/div[2]/div[1]/a/div/img[2]')

                    self.villa_data["Property Name"].append(name)
                    self.villa_data["Price"].append(price)
                    self.villa_data["Area"].append(area)
                    self.villa_data["Link"].append(link)
                    # self.images.append(image)
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


    def sort_by_price(self):
        list_of_lists = []
        sorted_data = []
        keys = list(self.villa_data.keys())

        if (self.searching_is_apartments == True):
            list_of_lists = [list(item) for item in zip(*self.apartment_data.values())]
            sorted_data = sorted(list_of_lists, key=lambda x: int((x[1].split(" ")[0].replace(',', ''))))
            print(sorted_data)
            self.apartment_data.clear()
            for item in sorted_data:
                for i, key in enumerate(keys):
                    self.apartment_data[key].append(item[i])
        else: 
            self.villa_data.clear()
            self.villa_data = {
            "Property Name": [],
            "Price": [],
            "Area": [], 
            "Link": [], 
            }
            for item in sorted_data:
                for i, key in enumerate(keys):   
                    # Append the corresponding item value to the list
                    self.villa_data[key].append(item[i])
            print(self.villa_data)


    def run_scraper(self, num_pages):
        self.open_website()

        if (self.searching_is_apartments == True):    
            self.set_search_apartment_criteria()
        else:
            self.set_search_villa_criteria()

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
            
            
        print(self.villa_data)
        print(self.apartment_data)
        print("------------------------------------------------------------------------------------------------------")
        self.sort_by_price()
       
        if (self.searching_is_apartments == True):   
            self.save_to_excel("apartment-properties.xlsx")
        else:
            self.save_to_excel("villa-properties.xlsx")


    def save_to_excel(self, file_name):
        if (self.searching_is_apartments == True):    
            df = pd.DataFrame(self.apartment_data)
        else:
            df = pd.DataFrame(self.villa_data)
        
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":

    # scraper_apartment = PropertyFinderSeleniumScraper()
    # scraper_apartment.run_scraper(num_pages=3)
    # scraper_apartment.close_browser()

    scraper_villa = PropertyFinderSeleniumScraper()
    scraper_villa.searching_is_apartments = False
    scraper_villa.run_scraper(num_pages=1)
    scraper_villa.close_browser() 
