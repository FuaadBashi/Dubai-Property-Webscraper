from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys




propertyfinder = "https://www.propertyfinder.ae"
service = Service("/Users/fuaad/Downloads/chromedriver")
location = "Dubai"
price = "150000"
page_number = 2


def open_propertyfinder(url=propertyfinder):
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(10)
    return driver



def find_properties(driver):
    property_area            = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/div/div/form/input")
    
    property_type            = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[1]")
    
    number_of_beds           = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[2]')

    search                   = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section[1]/div[2]/div/div[2]/button[3]')
    
    
    property_area.send_keys(location)

    # driver.implicitly_wait(2)
    property_type.click()
    driver.implicitly_wait(5)
    property_type_apartments = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/button[2]') 
    property_type_apartments.click()

    number_of_beds.click()
    number_of_beds_four      = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/ul/li[5]/button') 
    driver.implicitly_wait(5)
    number_of_beds_four.click()

    search.click()

def price_selection(driver):
    select_price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/button[3]')
    find = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button')

    select_price.click()
    input_price = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[2]/div/div/input')
    input_price.click()
    input_price.send_keys(price)

    confirm_click = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/p')
    confirm_click.click() 

    driver.implicitly_wait(5)

    done = driver.find_element(By.XPATH, '/html/body/div[7]/div/footer/button[2]')
    driver.implicitly_wait(5)
    # done.click()
   
    find.click()


def get_info_first_page(driver):

    properties_loc = []
    prices = []
    area = []

    for i in range(1, 30):
        if ( i == 6 or i == 7 or i == 13 or i == 19 or i == 20 or i == 26 or i == 28):
            continue

        find_price    = driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p')
       
        find_location =  driver.find_element(By.XPATH,f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p')
        

        find_area     = driver.find_element(By.XPATH,f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]')   

     

        properties_loc.append(find_location.text)
        prices.append(find_price.text)
        area.append(find_area.text)        
        print(i, "\n")                                        

    property_dict = {
    "name": properties_loc,
    "price": prices,
    "area": area 
    }

    print(property_dict)


def get_info_other_pages(driver):

    properties_loc = []
    prices = []
    area = []

    for i in range(1, 29):
        if ( i == 6 or i == 19 or i == 19 or i == 28):
            continue

        find_price    = driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[1]/div[1]/div/p')
       
        find_location =  driver.find_element(By.XPATH,f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[1]/p')
        

        find_area     = driver.find_element(By.XPATH,f'/html/body/div[1]/div/main/div[5]/div[1]/ul/li[{i}]/article/div/div/section[2]/div[2]/div[2]/p[3]')   

     

        properties_loc.append(find_location.text)
        prices.append(find_price.text)
        area.append(find_area.text)        
        print(i, "\n")                                        

    property_dict = {
    "name": properties_loc,
    "price": prices,
    "area": area 
    }

    print('\n')
    print(property_dict)

def next_page_see(driver):
    driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a').location_once_scrolled_into_view
   


def next_page(driver):
    next = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[5]/div[1]/div[4]/a')
    
    n = next.get_attribute ("href")
    driver.get(n)
    

driver = open_propertyfinder()

driver.maximize_window()

find_properties(driver)
price_selection(driver)
get_info_first_page(driver)
next_page_see(driver)
driver.implicitly_wait(5)
next_page(driver)
get_info_other_pages(driver)



#  6 , 17 ,24
