import re

import requests
import webbrowser

from Tools.scripts.generate_opcode_h import header
from bs4 import BeautifulSoup

html_string = """ 
              <!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test BeautifulSoup</title>
    <div id="produit">
        <ul>
            <li class="produit">Banane - 1€</li>
            <li class="produit">Pomme - 2€</li>
            <li class="produit">Orange - 1.5€</li>
        </ul>
    </div>
    <a href="https://example.com" class="liene">Visitez notre site</a>
</head>
<body>
    <h1>Bienvenue sur mon site de test</h1>
    <p class="description">Ceci est un simple fichier HTML pour tester le scraping.</p>

    <div id="produit">
        <ul>
            <li class="produit">Banane - 1€</li>
            <li class="produit">Pomme - 2€</li>
            <li class="produit">Orange - 1.5€</li>
        </ul>
    </div>

    <a href="https://example.com" class="lien">Visitez notre site</a>
</body>
</html>
"""

print( BeautifulSoup(html_string, ).head.title) # give the first title in head
print( BeautifulSoup(html_string, "lxml").head.parent.name )
print( BeautifulSoup(html_string , "html5lib").head )
print(BeautifulSoup(html_string, "lxml").body.div.ul.li.string) # nous doe le text

tag_a = BeautifulSoup(html_string).a
print(tag_a['href']) # affiche la valeur de l'attribut href dans letag
tag_a.attrs # permet de voir tous les attribuent associer a ce tag
tag_a.get_attribute_list('class') # donne les valeur de cette attribut

soup =  BeautifulSoup(html_string, "lxml")
soup.find("div", "produits",True)

soup =  BeautifulSoup(html_string, "lxml")
print(soup.find("div", "produits",))
print(soup.findAll(id = "produit")) # doenne tous les tag avec l'attribut src = "produit" return une list

print(soup.find(re.compile("^a"))) # return le premier tag  a link

for tag in soup.findAll(re.compile("^ul")):
    print(tag)


print(soup.find('a',attrs = {'class':re.compile('^lie')}))

for tag in soup.findAll('a',attrs = {'class':re.compile('^lie')}):
     print(tag)

soup.findAll(['a','img']) # retourne une liste avec tous les tag a et tous les tag img

print(soup.findAll(True)) # donne une list de tous les element tag de la racine juska la fin du dom tres importante

print(soup.findAll('a',href=True)) # donne tous les liens qui contienent href comme attribut

# ecrire une fonction personaliser qui affiche les tag avec pour attribut src et ne contient d'attribut href


"""
  nb tous les attribut d'un tag ou element renvoi comme valeur un string
  nb nous pouvons extraire uniquement des sous element comme des div 
  
  # ici le soupStrainer filtre par tag
  avec div_tags = soupStrainer("div")   soup = BeautifulSoup(html_code,"lxml", parse_only = div_tags)
  img_tags = soupStrainer("img")  soup = BeautifulSoup(html_code,"lxml", parse_only = imd_tags)
  
  # ici le soupSTrainer filtre par attribut
  alt_attr = SoupStrainer(alt = "creator_image")   soup = BeautifullSoup(html_code,"lxml", parse_only = alt_attr)
"""

def has_src_but_no_href(tag):
    return tag.has_attr('src') and not tag.has_attr('href')

print(soup.findAll(has_src_but_no_href))



def print_tag_with_src_and_no_href(soup):
    for tag in soup.findAll(re.compile('^a')):
        if has_src_but_no_href(tag):
            pass


while compteur < PAGE_COUNT:
    compteur+=1
    # click on the link with name shoes to print all shoes
    next_pag1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "pagination_pagination-link__AEkM_")]'))
     )
    next_pag1.click()

    # loop each item_articles
    for article in items_articles:
        list_nav_and_a = article.find_all(['nav', 'a'],
                                          {'data-testid': ['product-card-description-link', 'product-card-variations']})
        for item in list_nav_and_a:
            if 'product-card-description-link' in item['data-testid']:
                print("link:", item)
            else:
                print("navvvvvvvv")


def testweb(driver):
    page_count = 0
    PAGE_COUNT = 5

    while page_count < PAGE_COUNT:
        try:
            scroll_y = 0
            step = 300
            max_scroll = 8000  # pour éviter scroll infini
            next_button_found = False

            while scroll_y < max_scroll:
                driver.execute_script(f"window.scrollTo(0, {scroll_y});")
                time.sleep(1)

                try:
                    next_btn = driver.find_element(By.XPATH, '//button[@rel="next"]')
                    if next_btn.is_displayed():
                        next_button_found = True
                        break  # sortir du scroll dès que le bouton est visible
                except:
                    pass  # le bouton n'est pas encore dans le DOM ou visible

                scroll_y += step

            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            list_articles = soup.find_all("li", {"class": 's-grid__item'})
            print(f"Page {page_count + 1} - {len(list_articles)} articles trouvés.")

            find_product_categorie(list_articles)

            if next_button_found:
                wait = WebDriverWait(driver, 10)
                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@rel="next"]')))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                next_btn.click()
            else:
                print("Aucun bouton 'next' trouvé.")
                break

        except Exception as ex:
            print("Erreur:", ex)
            break

        finally:
            page_count += 1

        soup = BeautifulSoup(driver.page_source, "html.parser")
        all_articles = soup.find_all("li", {"class": 's-grid__item'})
        print(f"[Page {page_count + 1}] Articles visibles : {len(all_articles)}")

        # Sélectionner uniquement les nouveaux articles
        new_articles = all_articles[total_articles_seen:]
        print(f"→ Nouveaux articles trouvés : {len(new_articles)}")

        # Traitement des nouveaux articles
        find_product_categorie(new_articles)

        # Mise à jour du compteur total
        total_articles_seen = len(all_articles)
