import requests
from urllib.robotparser import RobotFileParser

BASE_URL = 'https://www.python.org'
ROBOTS_URL = f"{BASE_URL}/robots.txt"

# 1. Récupérer la page d'accueil avec Requests

response = requests.get(BASE_URL)

# 2. Afficher le code de statut
print("Code HTTP :", response.status_code)

# 3. Afficher les 500 premiers caractères du HTML

html = response.text
print("\n=== Aperçu du HTML (500 premiers caractères) ===")
print(html[:500])

# 4. Vérifier l'encodage de la page

print("\nEncodage détecté :", response.encoding)

# 5. Afficher les headers de la réponse

print("\n=== Headers de la réponse ===")
for key, value in response.headers.items():
    print(f"{key}: {value}")

# 6. Récupérer le robots.txt du site

def afficher_robots_txt():
    """Télécharge et affiche le contenu de robots.txt."""
    print(f"Récupération de {ROBOTS_URL} ...")
    response = requests.get(ROBOTS_URL)

    # Affichage brut du fichier robots.txt
    print("\n=== Contenu de robots.txt ===")
    print(response.text)

afficher_robots_txt()
# 7. **Bonus** : Utiliser une session pour faire 3 requêtes successives 

# Créer une session
session = requests.Session()

session.headers.update({'User-Agent': 'My Scraper 1.0'})

response1 = session.get(f"{BASE_URL}/blogs")
print("Response 1 : ")
print(response1.text[:100])
response2 = session.get(f"{BASE_URL}/doc")
print("Response 2 : ")
print(response2.text[:100])
response3 = session.get(f"{BASE_URL}/community")
print("Response 3 : ")
print(response3.text[:100])

session.close()