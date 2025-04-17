import csv
import re
import time
from datetime import datetime
import json

from Tools.scripts.texi2html import increment
from bs4 import BeautifulSoup
from colorlog import exception
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Set the number of pages to scrape
PAGE_COUNT = 2

# List of product categories to search
product_categories = [
    "Baumarkt", "Haushalt & Küche", "Wohnen", "Baby & Kind",
    "Multimedia", "Wein & Spirituosen", "Sport & Freizeit",
    "Gesundheit & Pflege"
]

product_categories1 = [
        "Baumarkt", "Wohnen", "Gesundheit & Pflege"

    ]

# Configure Chrome options to keep the browser open
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Lauch the chrome webdriver and navigate to the adidas website
driver = webdriver.Chrome(options=options)

driver.get("https://www.lidl.de/")
# wait containt page load
button_cookies = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
)
button_cookies.click()

# wait page print
time.sleep(10)


# Function to perform a search for each category and scroll through results
def search_and_scrape_each_category():
    for category in product_categories1:
        # Locate the search input field
        input_element = driver.find_element(By.ID, "s-search-input-field")

        # Clear any previous input
        input_element.clear()

        # Enter the category name into the search field
        input_element.send_keys(category)

        # Wait for suggestions or input stabilization
        time.sleep(10)

        # Press Enter to submit the search
        input_element.send_keys(Keys.RETURN)

        # Call the scrolling and scraping function for the current category
        scroll_through_results(category)




# Function to scroll through the product results and extract data from each page
def scroll_through_results(category):
    page_count = 0
    total_articles_seen = 0
    # Loop through result pages until the target page count is reached or no more pages are available
    while True :
        last_height = driver.execute_script("return window.pageYOffset")
        scroll_increment = 200
        scroll_down(scroll_increment, last_height)
        position_y = 2000
        driver.execute_script("window.scrollTo(0, arguments[0]);", position_y)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@rel="next"]'))).click()
        scroll_increment = driver.execute_script("return window.pageYOffset")
        scroll_down(scroll_increment,last_height)
        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        list_articles = soup.find_all("li", {"class": 's-grid__item'})
        # Select only new articles that haven't been seen before
        new_articles = list_articles[total_articles_seen:]
        total_articles_seen = len(list_articles)

        # Process and save articles to the CSV
        extract_and_save_products(new_articles, category)




        # Increment page count and continue to the next page
        #page_count += 1

def scroll_down(scroll_increment,last_height):
        while True:

            # Scroll down by incrementing the scroll position
            driver.execute_script(f"window.scrollTo(0, {scroll_increment});")
            time.sleep(1)  # Wait for lazy-loaded content to appear
            new_height = driver.execute_script("return window.pageYOffset;")

            # If the scroll position hasn't changed, we've reached the bottom of the page
            if new_height == last_height:
                break
            last_height = new_height
            scroll_increment += 200  # Increment scroll position for the next scroll

# Function to extract product information and save it into a CSV file
def extract_and_save_products(list_articles, category):
    # Open or create a CSV file for the specific category
    with open(f"{category}.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "subtitle", "description", "discount", "old_price", "new_price", "date", "images", "category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if writer:
            writer.writeheader()
        for item in list_articles:
            # Extract description and images
            description_product =  extract_product_description(item)
            images_dict = extract_all_product_images(item)

            # Extract individual fields
            title = item.find('div', {"class": "product-grid-box__brand"})
            subtitle = item.find('div', {"class": "product-grid-box__title"})
            discount = item.find('div', {"class": "m-price__label"})
            old_price = item.find('div', {"class": "strikethrough m-price__rrp m-price__text"})
            new_price = item.find('div', {"class": "m-price__price m-price__price--small"})

            # Create a dictionary for the product
            product = {
                "title": title.text.strip() if title else "N/A",
                "subtitle": subtitle.text.strip() if subtitle else "N/A",
                "description": json.dumps(description_product, ensure_ascii=False) if description_product else "N/A",
                "discount": discount.text.strip() if discount else "N/A",
                "old_price": old_price.text.strip() if old_price else "N/A",
                "new_price": new_price.text.strip() if new_price else "N/A",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "images": json.dumps(images_dict, ensure_ascii=False) if images_dict else "N/A",
                "category": category
            }

            # Write the product data to the CSV file
            writer.writerow(product)

            #print(product)



# Function to extract product description from an HTML element
def extract_product_description(item):
    description_product = {}
    key = None
    p_tag = item.find('p')

    if p_tag and p_tag.children:
        for elem in p_tag.children:
            if elem.name == 'strong':
                # Clean the field name (e.g., "Set:")
                key = elem.get_text(strip=True).replace(":", "")
            elif elem.name == 'img':
                # Use image src as the key if found
                key = elem['src']
            elif elem.name == 'br':
                continue
            elif key:
                # Extract the value and assign it to the key
                value = elem.strip() if isinstance(elem, str) else elem.get_text(strip=True)
                description_product[key] = value
                key = None  # Reset key for the next field

    return description_product


# Function to extract all product image URLs from an HTML item
def extract_all_product_images(item):
    images_dict = {}
    image_links = []

    # Find all image elements with the specified class
    image_elements = item.find_all("img", {"class": 'odsc-image-gallery__image'})

    # Collect the src attribute of each image
    for img in image_elements:
        image_links.append(img['src'])

    images_dict["images"] = image_links

    return images_dict






if __name__=="__main__":
    search_and_scrape_each_category()