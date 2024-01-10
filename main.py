from scraper import ZalandoScraper
from url_generator import generate_brand_urls

# Example of scraping dameskleding
if __name__ == "__main__":
    main_category_url = 'https://www.zalando.nl/dameskleding/'
    brand_urls_dict = generate_brand_urls(main_category_url)
    webdriver_path = r'C:\webdrivers\chromedriver.exe'

    # Initialize and run the scraper
    scraper = ZalandoScraper(webdriver_path, brand_urls_dict)
    scraper.scrape_data()