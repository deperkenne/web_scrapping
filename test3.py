import time

from bs4 import BeautifulSoup
from lxml.etree import XPath
from markdown_it.common.html_re import attribute
from selenium import  webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Garde la fenêtre ouverte

driver = webdriver.Chrome(options=options)
driver.get("https://www.adidas.de/")

driver.find_element(By.XPATH ,'//button[@id="glass-gdpr-default-consent-accept-button"]').click()
time.sleep(1)
driver.find_element(By.XPATH ,'//a[@href="/schuhe"]').click()
time.sleep(1)
driver.find_element(By.XPATH ,'//article[@data-testid="plp-product-card"]').click()
time.sleep(1)
driver.find_element(By.XPATH ,'//a[@data-testid="product-card-description-link"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//footer[@data-testid="plp-product-card"]').click()


