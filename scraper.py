import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

class ZalandoScraper:
    def __init__(self, webdriver_path, brand_urls_dict):
        # Initialize the ZalandoScraper with the provided webdriver path and brand URLs dictionary
        self.brand_urls_dict = brand_urls_dict
        self.driver = self.setup_driver(webdriver_path)

    def setup_driver(self, webdriver_path):
        # Set up the Chrome WebDriver with specific options
        service = Service(webdriver_path)
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode (without UI)
        options.add_argument("--window-size=1920,1080")  # Set window size
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--blink-settings=imagesEnabled=false")  # Disable loading images
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")  # Set user-agent
        return webdriver.Chrome(service=service, options=options)

    def scroll_to_bottom(self):
        # Scroll to the bottom of the page using JavaScript
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

    def scrape_data(self, filename='scraped_data'):
        # Get the current date and time for creating a unique filename
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f'{filename}_{current_date}.csv'

        for main_brand_url, brand_urls in self.brand_urls_dict.items():
            for brand_url in brand_urls:
                with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    # If the CSV file is empty, write the header row
                    if csv_file.tell() == 0:
                        csv_writer.writerow(['title', 'brand', 'url', 'disc_price', 'original_discount_price', 'price', 'image_url', 'main_brand_url', 'brand_url', 'rank', 'date'])

                    # Open the brand URL in the WebDriver and wait for elements to load
                    self.driver.get(brand_url)
                    self.driver.implicitly_wait(4)

                    # Extract information about the number of pages from the page source
                    page_source = self.driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    element = soup.select('[id="main-content"] div div:nth-of-type(7) div div:nth-of-type(2) nav div span')
                    scraped_data = element[0].text
                    matches = re.findall(r'\d+', scraped_data)
                    last_number = int(matches[-1])

                    # Iterate over each page of the brand URL
                    for page_num in range(1, last_number + 1):
                        current_url = f'{brand_url}?p={page_num}'
                        self.driver.get(current_url)
                        self.driver.implicitly_wait(10)

                        # Scroll to the bottom of the page to load more products
                        self.scroll_to_bottom()

                        # Extract product information from the HTML source
                        html = self.driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        products = soup.find_all('div', class_='_5qdMrS w8MdNG cYylcv BaerYO _75qWlu iOzucJ JT3_zV _Qe9k6')

                        # Iterate over each product on the page
                        for product in products:
                            skus = product.find('a', class_="_LM JT3_zV CKDt_l CKDt_l LyRfpJ")
                            title = product.find('h3', class_='sDq_FX lystZ1 FxZV-M HlZ_Tf ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2')
                            disc_price = product.find('p', class_='sDq_FX lystZ1 dgII7d HlZ_Tf')
                            brand = product.find('h3', class_='FtrEr_ lystZ1 FxZV-M HlZ_Tf ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2')
                            orig_disc_price = product.find('p', class_='sDq_FX _2kjxJ6 FxZV-M HlZ_Tf _0xLoFW _7ckuOK')
                            orig_price = product.find('p', class_='sDq_FX lystZ1 FxZV-M HlZ_Tf')
                            img_tags = product.find('img', class_="sDq_FX lystZ1 FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF _7ZONEy")

                            # Extract and handle product details
                            if title:
                                img_url = img_tags["src"]

                                try:
                                    disc_price_text = disc_price.text
                                except AttributeError:
                                    disc_price_text = "N/A"

                                try:
                                    orig_disc_price_text = orig_disc_price.text
                                except AttributeError:
                                    orig_disc_price_text = "N/A"

                                try:
                                    orig_price_text = orig_price.text
                                except AttributeError:
                                    orig_price_text = "N/A"

                                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                                # Write product details to the CSV file
                                csv_writer.writerow([
                                    title.text, brand.text, skus.attrs['href'], disc_price_text, orig_disc_price_text, orig_price_text, img_url,
                                    main_brand_url, brand_url, page_num, current_datetime
                                ])

        # Close the WebDriver
        self.driver.quit()

