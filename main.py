import smtplib
import requests
import lxml
from bs4 import BeautifulSoup

url = "https://www.bayut.com/to-rent/property/dubai/?ipckg=true&rent_frequency=any&utm_source=google&utm_medium=cpc&utm_campaign=%7Bcampaignname%7D&gclid=CjwKCAiA65m7BhAwEiwAAgu4JGU5idzaYqbPVmXinDPZ7aI4cE64664Wq6IHqNVTce1xHj0Tfwie-RoCArUQAvD_BwE"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)
# soup = BeautifulSoup(response.content, 'html.parser')

if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())

    # Extract property names and prices
    properties = []
    Area = []
    prices = []

    for listing in soup.find_all( class_="a37d52f0"): 
        for price in soup.find_all( class_="dc381b54"):  
            prices.append(price.text)

        for property in soup.find_all( class_="_948d9e0a _371e9918"):
            properties.append(property.text)
        
        for size in soup.find_all( class_="_19e94678 f8d4dd58"):
            Area.append(size.text)
        

    property_dict = {
    "name": properties,
    "price": prices,
    "area": Area 
    }

    print(property_dict)
    # Print the extracted properties
    for name, price, area in zip(property_dict["name"], property_dict["price"], property_dict["area"]):
        print(f"Property Name: {name},  Price: {price} AED Per month , Area: {area}" )


else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
