# Dubai-Property-Webscraper
A powerful Python script utilizing Selenium and BeautifulSoup to scrape real estate data from [Property Finder UAE](https://www.propertyfinder.ae) and [Bayut](https://www.bayut.com). This tool provides details such as property names, prices, and areas, enabling efficient data collection for property analysis and research.  


```markdown
# Real Estate Scraper

Real Estate Scraper is a Python project that automates the extraction of property details from leading real estate websites like Property Finder and Bayut. This script uses **Selenium** for dynamic content handling and **BeautifulSoup** for efficient parsing of static web pages.

## Features

- **Supports Multiple Platforms:** 
  - [Property Finder UAE](https://www.propertyfinder.ae)
  - [Bayut](https://www.bayut.com)
  
- **Dynamic Search Capabilities:**
  - Customizable search parameters such as location, price range, and number of bedrooms.

- **Data Extraction:**
  - Scrapes property names, prices, and areas.
  - Handles dynamic web elements with Selenium.
  - Extracts static content with BeautifulSoup.

- **Error Handling:**
  - Handles exceptions like stale elements and missing data gracefully.

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver matching your Chrome version
- Required Python libraries:
  - `selenium`
  - `bs4`
  - `requests`
  - `lxml`

Install dependencies using pip:

```bash
pip install selenium beautifulsoup4 requests lxml
```

## How to Use

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/real-estate-scraper.git
   cd real-estate-scraper
   ```

2. **Setup ChromeDriver:**

   Download the [ChromeDriver](https://chromedriver.chromium.org/) compatible with your Chrome browser and update the `service` variable in the script:

   ```python
   service = Service("/path/to/chromedriver")
   ```

3. **Customize Search Parameters:**

   Modify the search criteria in the script:

   ```python
   location = "Dubai"
   price = "150000"
   page_number = 2
   ```

4. **Run the Script:**

   Execute the script:

   ```bash
   python real_estate_scraper.py
   ```

5. **View Extracted Data:**

   Scraped data will be printed to the console in a dictionary format.

## Example Output

For Property Finder:

```json
{
  "name": ["Luxury Villa in Dubai", "Modern Apartment"],
  "price": ["150,000 AED", "200,000 AED"],
  "area": ["2,500 sqft", "1,800 sqft"]
}
```

For Bayut:

```json
{
  "name": ["Spacious Studio", "Penthouse in Marina"],
  "price": ["50,000 AED", "500,000 AED"],
  "area": ["800 sqft", "10,000 sqft"]
}
```

## Disclaimer

This project is intended for educational purposes only. Ensure compliance with the terms of service of the target websites before running the scraper.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

You can replace placeholders like `yourusername` in the repository URL with your actual GitHub username. Let me know if you'd like further customizations or assistance with your project!
