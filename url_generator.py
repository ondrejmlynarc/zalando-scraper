from bs4 import BeautifulSoup
import requests


def generate_brand_urls(main_category_url):
    # Send a GET request to the main category URL
    response = requests.get(main_category_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    ul_elements = soup.find_all('ul', class_='ODGSbs')

    links = []
    visited_links = set()
    for ul_element in ul_elements:
        anchor_tags = ul_element.find_all('a', class_='_ZDS_REF_SCOPE_')
        href_values = [tag.get('href') for tag in anchor_tags]
        links.extend(href_values)

    # Check if there are any links
    if links:
        result_dict = {}

        # Iterate over each link extracted from the main category URL
        for link in links:
            response = requests.get(link)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                ul_elements = soup.find_all('ul', class_='ODGSbs')

                links2 = []
                for ul_element in ul_elements:
                    anchor_tags = ul_element.find_all('a', class_='_ZDS_REF_SCOPE_')
                    href_values = [tag.get('href') for tag in anchor_tags]
                    links2.extend(href_values)

                # Filter out links2 that are not in links
                links2 = [sub_link for sub_link in links2 if sub_link not in links]
                links2 = list(set(links2))

                # If links2 is empty, add the main category (link) to its values
                if not links2:
                    links2.append(link)

                # Assign links2 as values for the current link in the result dictionary
                result_dict[link] = links2

        # The result_dict now contains each link from 'links' as keys, and their corresponding 'links2' as values,
        return result_dict
