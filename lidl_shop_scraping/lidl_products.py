import csv
import re
import time
from datetime import datetime
import json
from Demos.BackupSeek_streamheaders import tempfile
from bs4 import BeautifulSoup
from lxml.etree import XPath
from markdown_it.common.html_re import attribute
from scripts.regsetup import description
from selenium import  webdriver

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# set the number of pages to scrape
#PAGE_COUNT = int(input(" Enter number of pages to be scraped: "))

PAGE_COUNT = 200
list_categories = ["garten & Balkon"]
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

def find_categorie():

    for categorie in list_categories:
        input_element = driver.find_element(By.ID, "s-search-input-field")
        input_element.clear()
        input_element.send_keys(categorie)
        time.sleep(2)
        input_element.send_keys(Keys.RETURN)
        scroll_website(categorie)







def scroll_website(categorie):
    page_count = 0
    total_articles_seen = 0
    activ_bool = False


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
            scroll_increment = scroll_increment + 200

        try:

            # Find the link to the next page
            position_y = 2000
            driver.execute_script("window.scrollTo(0, arguments[0]);", position_y)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@rel="next"]'))).click()
            time.sleep(3)



        except Exception  as  ex:
            activ_bool = True
            break

        finally:
            # parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            list_articles = soup.find_all("li", {"class": 's-grid__item'})
            # Sélectionner uniquement les nouveaux articles
            new_articles = list_articles[total_articles_seen:]
            # Mise à jour du compteur total
            total_articles_seen = len(list_articles)
            find_product_categorie(new_articles, categorie)
            if activ_bool == True:
                page_count = 300
            else:
                page_count += 1


def find_product_categorie(list_articles,categorie):
    products = {}



    # Open 'Shoes_listings.csv' file for writing the scraped data
    with open(f"{categorie}.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "subtitle", "description", "discount", "old_price", "new_price","date","images","categorie"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list_articles:
            description_product = give_product_descption_contain(item)
            images_dict = give_all_product_image(item)

            title = item.find('div', {"class": "product-grid-box__brand"})
            subtitle = item.find('div', {"class": "product-grid-box__title"})
            discount = item.find('div', {"class": "m-price__label"})
            old_price = item.find('div', {"class": "strikethrough m-price__rrp m-price__text"})
            new_price = item.find('div', {"class": "m-price__price m-price__price--small"})

            products["title"] = title.text.strip() if title else "N/A"
            products["subtitle"] = subtitle.text.strip() if subtitle else "N/A"
            products["description"] = json.dumps(description_product, ensure_ascii=False) if len(description_product)>0 else "N/A"
            products["discount"] = discount.text.strip() if discount else "N/A"
            products["old_price"] = old_price.text.strip() if old_price else "N/A"
            products["new_price"] = new_price.text.strip() if new_price else "N/A"
            products["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            products["images"] = json.dumps(images_dict, ensure_ascii=False) if len(images_dict)>0 else "N/A"
            products["categorie"] = categorie

            writer.writerow(products)





       # writer.writerow(products)

def give_product_descption_contain(item):
    description_product = {}
    key = None
    p_tag = item.find('p')
    if p_tag and p_tag.children:
        for elem in p_tag.children:
            if elem.name == 'strong':
                # Nettoie le nom de champ (ex: "Set:")
                key = elem.get_text(strip=True).replace(":", "")
            elif elem.name == 'img':
                key = elem['src']
            elif elem.name == 'br':
                continue
            elif key:
                # Enlève les espaces et associe la valeur
                value = elem.strip() if isinstance(elem, str) else elem.get_text(strip=True)
                description_product[key] = value
                key = None  # Reset pour le champ suivant
    return description_product

def give_all_product_image(item):
    images_dict = {}
    list_link = []
    first_product = item.find_all("img", {"class": 'odsc-image-gallery__image'})
    for img in first_product:
        list_link.append(img['src'])
    images_dict["images"] = list_link

    return images_dict

def shoes_scrapped():

    try:


        time.sleep(5)
        input_element = driver.find_element(By.ID, ":rh:")
        input_element.clear()
        input_element.send_keys("Berlin")
        time.sleep(2)
        input_element.send_keys(Keys.RETURN)
        print("clic sur l'input reussi.")



        # Sélectionner les dates
        button_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="date-display-field-start"]'))
        )
        button_date.click()

        print("testtttt")

        # Sélectionner les dates
        button_check = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@tabindex="0"]'))
        )
        button_check.click()
        print("okkkkk")
        #checkin_input.send_keys("So.,23.Feb")  # Format JJ-MM-AAAA
        #time.sleep(10)
        # parse the page source with BeautifulSoup


        # Sélectionner les dates
        button_check1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@tabindex="0"]'))
        )
        button_check1.click()
        time.sleep(3)
        # Sélectionner les dates
        button_check2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="24 Februar 2025"]'))
        )
        button_check2.click()

        time.sleep(10)

        # Sélectionner les dates
        button_suche = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        button_suche.click()

        soup = BeautifulSoup(driver.page_source, "html.parser")

        list_articles = soup.find("button", {"data-testid": 'date-display-field-start'})
        print(list_articles)
    except Exception as e:
        print("error:",e)

    #driver.get("https://www.adidas.de/")
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

    #data_scrapped_and_save_to_csv(driver)


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
                wait.until(EC.element_to_be_clickable(By.XPATH,'//button[@class="s-load-more__hidden-tex"]'))

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




                time.sleep(5)

                page_count+=1
                print("Next Page:",page_count)


if __name__=="__main__":
    find_categorie()