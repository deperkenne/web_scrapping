import csv
import re

from bs4 import BeautifulSoup
from lxml.etree import XPath
from markdown_it.common.html_re import attribute
from selenium import  webdriver

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Garde la fenêtre ouverte

driver = webdriver.Chrome(options=options)
driver.get("https://www.adidas.de/schuhe")


list_elements_articles = driver.find_elements(By.TAG_NAME,"article")
for i, article in enumerate(list_elements_articles[:10], start=1):
    soup_list = BeautifulSoup(article.get_attribute("innerHTML"), "lxml").findAll(re.compile('^a'))
    for link in soup_list:
        soup = link.find(re.compile('^footer'))
        if soup :
          print(soup)
          # Extraction des éléments souhaités en ciblant les attributs data-testid (plus fiables que les classes dynamiques)
          price_element = soup.find('div', {'data-testid': 'primary-price'})
          title_element = soup.find('p', {'data-testid': 'product-card-title'})
          subtitle_element = soup.find('p', {'data-testid': 'product-card-subtitle'})
          badge_element = soup.find('p', {'data-testid': 'product-card-badge'})

          # On vérifie que chaque élément a bien été trouvé et on récupère le texte en nettoyant les espaces éventuels
          price = price_element.text.strip() if price_element else ""
          title = title_element.text.strip() if title_element else ""
          subtitle = subtitle_element.text.strip() if subtitle_element else ""
          badge = badge_element.text.strip() if badge_element else ""

          # Création d'une liste de données (ici, une seule ligne – vous pouvez l'étendre pour plusieurs produits)
          data = [[price, title, subtitle, badge]]

          # Écriture dans un fichier CSV
          with open("produits.csv", "a+", newline="", encoding="utf-8") as csvfile:
              writer = csv.writer(csvfile)
              # Écriture de l'en-tête
              writer.writerow(["Prix", "Titre", "Sous-titre", "Badge"])
              # Écriture des données
              writer.writerows(data)

driver.quit()





"""
element_css = driver.find_element(By.CSS_SELECTOR,'#run.button') # ici on cherche le selecteur #run et on recupere les button
element_css1 = driver.find_element(By.LINK_TEXT,"electro")

# "XPath = //tagname[@attribute="value"]" format du xPath
# find_elements() return list list de tous element qui coincide avec le filtre
# find_element() return une variable c'est le premier qui coincide avec le fitre
# find_element(By.XPATH, '//div[contains[@class, "Pagination_srp")]//a[contains(@class, "list_header_bold")]'

"""

