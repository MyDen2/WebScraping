from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = "http://quotes.toscrape.com"

# 1. Récupérer la page d'accueil

response = requests.get(BASE_URL)

# Parser avec BeautifulSoup

soup = BeautifulSoup(response.text, "lxml")


def extract_data_quote(soup):
    all_quotes = soup.find_all(class_='quote')
    result = []
    for quote in all_quotes:
        text = quote.find(class_='text').get_text()
        tags = quote.find('meta')['content']
        author = quote.find(class_='author').get_text()
        result.append({
            'Quote': text,
            'Tags': tags,
            'Auteur': author
        })
    return result

number_of_pages = 0
data = []
def detection_number_of_pages(url, number_of_pages):
    number_of_pages +=1
    print(url)
    try: 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        
        data.extend(extract_data_quote(soup))

        classe = soup.find(class_='next')
        link = classe.find("a")["href"]

        if link:
            url = link
            detection_number_of_pages(f"{BASE_URL}{link}", number_of_pages)
    except Exception as e : 
            print(f" Nombre de pages : {number_of_pages}") 

detection_number_of_pages(BASE_URL, number_of_pages)

df = pd.DataFrame(data)
df['Taille citation'] = df['Quote'].str.len()

df3 = df.explode("Tags")["Tags"].value_counts().reset_index()
df3.columns = ["Tag", "Fréquence"]

df2 = df.groupby("Auteur")["Quote"].count().reset_index()
df2.columns = ["Auteur", "Nombre_de_quotes"]

with pd.ExcelWriter('citations.xlsx') as writer:
    df.to_excel(writer, sheet_name='Citations', index=False)
    df2.to_excel(writer, sheet_name='Auteurs', index=False)
    df3.to_excel(writer, sheet_name='Tags', index=False)

# 5. Génère des statistiques :

top_five_authors = df2.nlargest(5, "Nombre_de_quotes")
print(top_five_authors)

top_ten_tags = df3.nlargest(5, "Fréquence")
print(top_ten_tags)

average_len = df['Taille citation'].mean()
print(average_len)