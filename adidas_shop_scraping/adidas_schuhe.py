import csv
import re
import time

from bs4 import BeautifulSoup
from lxml.etree import XPath
from markdown_it.common.html_re import attribute
from selenium import  webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Garde la fenêtre ouverte


# set the number of pages to scrape
PAGE_COUNT = int(input("Enter number of pages to be scraped: "))

# Lauch the chrome webdriver and navigate to the adidas website
driver = webdriver.Chrome(options=options)
driver.get("https://www.adidas.de/")

# click on the button to open main page
driver.find_element(By.XPATH ,'//button[@id="glass-gdpr-default-consent-accept-button"]').click()
time.sleep(1)

# click on the link with name shoes to print all shoes
driver.find_element(By.XPATH ,'//a[@href="/schuhe"]').click()
time.sleep(1)

# Open 'Shoes_listings.csv' file for writing the scraped data
with open("shoes_listings.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["price", "title", "subtitle", "badge"]
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()

    page_count = 0

    # start a loop that will continue until the desired number of page have bee scraped

    while page_count < PAGE_COUNT:
        # Scroll down the page incrementally to load all property
        last_height = driver.execute_script("return window.pageYOffset")
        scroll_increment = 200

        while True:
            driver.execute_script("window.scrollTo(0, {});".format(scroll_increment))
            time.sleep(1)
            new_height = driver.execute_script("return window.pageYOffset;")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_increment = scroll_increment + 300

        # Find the link to the next page
        next_page = driver.find_element(By.XPATH, '//div[contains(@class,"pagination_next_d4M5T")]//a[contains(@class, "pagination_pagination-link_AEKM")]')[1]

        # parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source,"html.parser")

        # Find all property listings on the current page
        items = soup.find_all('footer',{'class':["product-card-description_product-card-details__zFLlG"]})

        # loop each items
        for item in items:
            shoes = {}

            if "product-card__product-card__a9BIh" in item["class"]:
                fieldnames = ["price", "title", "subtitle", "badge"]
                shoes["price"] = item.find('div', {"class": "gl-price-item"}).text
                shoes["title"] = item.find('p', {'data-testid': 'product-card-title'}).text
                shoes["subtitle"] =  item.find('p', {'data-testid': 'product-card-subtitle'}).text
                shoes["badge"] = item.find('p', {'data-testid': 'product-card-badge'}).text

