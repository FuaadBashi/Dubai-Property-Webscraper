# Dubai-Property-Webscraper

A Python-based scraper designed to extract property listings from **Bayut** and **Property Finder** websites. The project utilizes both **BeautifulSoup** and **Selenium** to gather real estate information such as property names, prices, and areas. The data is displayed in the terminal and optionally saved to an Excel file.

## Features

- **Bayut Scraper**: Uses `BeautifulSoup` for HTML parsing to scrape data from Bayut.
- **Property Finder Scraper**: Employs `Selenium` for dynamic web interactions and data extraction from Property Finder.
- Saves scraped data to an Excel file for easy sharing and analysis.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

Ensure you have Python installed (preferably 3.7+). Install required libraries using `pip`:

```bash
pip install requests beautifulsoup4 lxml selenium pandas openpyxl
```

### WebDriver

For Selenium:
1. Download the [ChromeDriver](https://chromedriver.chromium.org/downloads) that matches your Chrome version.
2. Place it in a directory accessible to your Python script.

---

## Usage

### Bayut Scraper

1. Update the `URL` and `HEADERS` in the `BayutBeautifulSoupScraper` class.
2. Run the script:

```bash
python bayut_scraper.py
```

3. The scraped data will be displayed in the terminal.

### Property Finder Scraper

1. Update the `location` and `max_price` parameters in the `PropertyFinderSeleniumScraper` class.
2. Adjust file paths for the `ChromeDriver`.
3. Run the script:

```bash
python property_finder_scraper.py
```

4. The script will scrape the data and save it to `properties.xlsx`.

---

## Code Structure

### `bayut_scraper.py`
- **`BayutBeautifulSoupScraper`**: Handles static HTML scraping with BeautifulSoup.

### `property_finder_scraper.py`
- **`PropertyFinderSeleniumScraper`**: Uses Selenium for dynamic website interactions.
- Features page navigation, filtering, and Excel file generation.

---

## Requirements

| Library            | Version     |
|--------------------|-------------|
| Python             | 3.7+        |
| requests           | Latest      |
| beautifulsoup4     | Latest      |
| lxml               | Latest      |
| pandas             | Latest      |
| selenium           | Latest      |
| openpyxl           | Latest      |

---

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to let me know if you need further tweaks or enhancements!
