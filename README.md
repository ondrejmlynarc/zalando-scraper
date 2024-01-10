# Zalando Scraper

The Zalando Scraper is a Python application designed to extract product information from Zalando's website using web scraping techniques. The scraper is built using Selenium and BeautifulSoup, making it capable of navigating through pages, extracting data, and storing it in a CSV file.

## Features

- **Dynamic Web Scraping:** The scraper uses Selenium to dynamically navigate through Zalando's web pages, allowing it to handle paginated content and extract comprehensive product information.

- **Data Storage:** Extracted product details, including title, brand, URL, prices, image URLs, and more, are stored in a CSV file for easy analysis and further processing.

- **Customizable:** The scraper is designed to be adaptable. You can easily customize the main URLs and subcategory URLs to target specific sections of Zalando's product offerings.

## Prerequisites

Before using the Zalando Scraper, ensure that you have the following installed:

- Python 3.x
- Selenium
- BeautifulSoup
- Chrome WebDriver

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/zalando-scraper.git


2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Configure the scraper:**
Update the webdriver_path variable in main.py with the path to your Chrome WebDriver.

4. **Run the scraper::**

   ```bash
   python main.py
   

## Usage Notes 
- **Customization**: Modify the urls_dict variable in main.py to target specific Zalando categories and subcategories.

- **WebDriver**: Ensure that the Chrome WebDriver path is correctly configured for your system.

- **Data Output**: The scraped data is saved in CSV format for easy integration into various data analysis tools.