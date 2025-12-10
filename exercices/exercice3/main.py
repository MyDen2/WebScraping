from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

url = "http://books.toscrape.com"

# 1. Récupérer la page d'accueil

response = requests.get(url)

# Parser avec BeautifulSoup

soup = BeautifulSoup(response.text, "lxml")

# 2

data_books = []

books = soup.find_all(class_="product_pod")
print(books)
for book in books: 
    image = book.find(class_="thumbnail")
    print(f"imgae {image}")
    url_image = image["src"]
    title = book.find("h3").get_text()
    price = float(book.find(class_="price_color").get_text()[2:])
    rate = book.find("p")["class"][1]
    availability = book.find(class_="instock availability").get_text(strip=True)
    availability = " ".join(availability.split())
    data_books.append({
        'Titre' : title,
        'Prix' : price,
        'Note' : rate, 
        'Disponibilité' : availability,
        'URL de l\'image' : f"{url}/{url_image}"
    })

#print(data_books)

df = pd.DataFrame(data_books)

#print(df)

# Prix moyen 

average_price = df["Prix"].mean()
#print(average_price)

# Livre le plus cher

most_expensive_book = df.nlargest(1, 'Prix')
print(f"Most expensive book {most_expensive_book}")

# Livre le moins cher

less_expensive_book = df.nsmallest(1, 'Prix')
#print(f"Less expensive book {less_expensive_book}")

# Répartition par note

rate_repartition = df.sort_values("Note", ascending=False)
#print(f"Répartition par note : {rate_repartition}")

# 5. Sauvegarder dans `books.csv`

df.to_csv("books.csv", index=False)

# 6. **Bonus** : Télécharger l'image du livre le plus cher

# 4) Fonction de téléchargement d'une image
def download_image(image_url, save_path):
    response = requests.get(image_url)
    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)

# 

print(f"Livre le plus cher : {most_expensive_book}")

most_expensive_book_url = most_expensive_book['URL de l\'image'].values[0]
download_image(most_expensive_book_url, "data/output/image_du_livre_le_plus_cher.jpg")