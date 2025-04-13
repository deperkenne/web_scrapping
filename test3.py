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



# Function to scroll through the product results and extract data from each page
def scroll_through_results(category):
    page_count = 0
    total_articles_seen = 0
    # Loop through result pages until the target page count is reached or no more pages are available
    while page_count < PAGE_COUNT :
        last_height = driver.execute_script("return window.pageYOffset")
        scroll_increment = 200

        while True:

                try:

                        # Wait until the "Next" button becomes visible and click it
                        next_button = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, '//button[@rel="next"]'))
                        )
                        if next_button.is_displayed():
                            next_button.click()
                            time.sleep(3)

                except Exception as e:
                    print("uncheck exception",e.__str__())
                    break
                finally:
                    # Scroll down by incrementing the scroll position
                    driver.execute_script(f"window.scrollTo(0, {scroll_increment});")
                    time.sleep(1)  # Wait for lazy-loaded content to appear
                    new_height = driver.execute_script("return window.pageYOffset;")

                    # If the scroll position hasn't changed, we've reached the bottom of the page
                    if new_height == last_height:
                        break
                    last_height = new_height
                    scroll_increment += 800  # Increment scroll position for the next scroll

        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        list_articles = soup.find_all("li", {"class": 's-grid__item'})

        # Select only new articles that haven't been seen before
        new_articles = list_articles[total_articles_seen:]
        total_articles_seen = len(list_articles)

        # Process and save articles to the CSV
        extract_and_save_products(new_articles, category)

        # Increment page count and continue to the next page
        page_count += 1


