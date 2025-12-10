from bs4 import BeautifulSoup
import requests
import json

url = "http://quotes.toscrape.com"

# 1. Récupérer la page d'accueil

response = requests.get(url)

# 2. Parser avec BeautifulSoup

soup = BeautifulSoup(response.text, "lxml")

# 3. Trouver toutes les citations (class="quote")

quotes = soup.find_all(class_="quote")

# 4. Pour chaque citation, extraire :
#    - Le texte de la citation
#    - L'auteur
#    - Les tags

quotes_data = []
list_tag = []
for quote in quotes: 
    text = quote.find(class_="text").text
    author = quote.find(class_="author").text
    tags = quote.find_all(class_="tag", limit = 2)
    for tag in tags :
        list_tag.append(tag.get_text(separator=' '))
    quotes_data.append({
        'Texte' : text,
        'Auteur' : author,
        'Tag' : list_tag
    })

# 5. Afficher les 5 premières citations

first_five_quotes = soup.find_all(class_="quote", limit=5)
list_first_five_quotes = []
for quote in first_five_quotes:
    list_first_five_quotes.append(quote.find(class_="text").text)
#print(f"Afficher les 5 premières citations : {list_first_five_quotes} et son type {type(list_first_five_quotes)}")

# 6. Compter le nombre total de citations sur la page

total_number_quotes = len(soup.find_all(class_="quote"))
print(soup.find_all(class_="quote"))
print(type(soup.find_all(class_="quote")))
#print(f"Nombre total de citations : {total_number_quotes} et son type {type(total_number_quotes)}")

# 7. Créer une liste de dictionnaires avec les données

data = [{
     'Citations' : quotes_data,
     'Cinq premieres citations' : list_first_five_quotes,
     'Nombre total de citations' : total_number_quotes
}]

#**Bonus** : Sauvegarder dans un fichier JSON
with open("recap.json", "w", encoding= "utf-8")as f:
    json.dump(data, f, ensure_ascii= False, indent = 4)
