import csv
import re
import time
from datetime import datetime

from bs4 import BeautifulSoup
from lxml.etree import XPath
from markdown_it.common.html_re import attribute
from selenium import  webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# set the number of pages to scrape
#PAGE_COUNT = int(input(" Enter number of pages to be scraped: "))

PAGE_COUNT = 1

def shoes_scrapped():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    # Lauch the chrome webdriver and navigate to the adidas website
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.adidas.de/")
    # click on the button to open main page
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="glass-gdpr-default-consent-accept-button"]'))
    )
    button.click()

    # click on the link with name shoes to print all shoes
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="/schuhe"]'))
    )
    element.click()

    data_scrapped_and_save_to_csv(driver)


def data_scrapped_and_save_to_csv(driver):

        # Open 'Shoes_listings.csv' file for writing the scraped data
        with open("shoes_listings.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["price", "title", "subtitle", "number_of_color","badge","date","url"]
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
                    scroll_increment = scroll_increment + 800

                # Find the link to the next page
                position_y = 4000

                driver.execute_script("window.scrollTo(0, arguments[0]);", position_y)
                wait = WebDriverWait(driver,20)
                wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"WEITER"))).click()

                time.sleep(10)
                # parse the page source with BeautifulSoup
                soup = BeautifulSoup(driver.page_source,"html.parser")

                list_articles = soup.find_all("article",{"class":'product-grid_product-card__8ufJk'})
                print(len(list_articles))
                shoes = {}
                for item in list_articles:
                    footer = item.find(re.compile("^footer"))
                    price = footer.find('div', {"class": "gl-price-item"})
                    title = footer.find('p', {'data-testid': 'product-card-title'})
                    subtitle = footer.find('p', {'data-testid': 'product-card-subtitle'})
                    number_of_color = footer.find('p', {'data-testid': 'product-card-colours'})
                    badge = footer.find("p", {'class': "product-card-description_badge__m75SV"})
                    link = item.find(re.compile("^a"))
                    url = "https://" + link["href"].lstrip('/')

                    shoes["url"] = url.strip() if url else "N/A"
                    shoes["price"] = price.text.split(" ")[1].strip() if price else "N/A"
                    shoes["title"] = title.text.strip() if title else "N/A"
                    shoes["subtitle"] = subtitle.text.strip() if subtitle else "N/A"
                    shoes["number_of_color"] = number_of_color.text.strip() if number_of_color else "N/A"
                    shoes ["badge"] = badge.text.strip() if badge else "N/A"
                    shoes["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                    writer.writerow(shoes)
                    print(shoes)



                time.sleep(5)

                page_count+=1
                print("Next Page:",page_count)


if __name__=="__main__":
    shoes_scrapped()