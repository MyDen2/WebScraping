import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import time
import pandas as pd
from src.utils.logger import setup_logger

BASE_URL = 'http://quotes.toscrape.com'

logger = setup_logger('Logger_WebScraping', 'logs/etl.log')

# 1. Créer une fonction `fetch_page(url)` avec gestion d'erreurs

def fetch_page(url, timeout=10):
    """Récupère une page avec gestion d'erreurs."""
    try:
        logger.info("===== CREATION SESSION : =====")
        session = requests.Session()
        logger.info("===== RECUPERATION DE LA PAGE : =====")
        response = session.get(
            url,
            timeout=timeout
        )
        # Lève une exception si le code HTTP est 4xx ou 5xx
        response.raise_for_status()
        return [response.text, response.status_code, len(response.content)]

    except Timeout:
        logger.error(f"Timeout pour {url}")
        return None

    except ConnectionError:
        logger.error(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        logger.error(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        logger.error(f"Erreur générale: {e}")
        return None

def main():
    data = []
    for i in range(1,4):
        start_time = time.time()
        url = f"{BASE_URL}/page/{i}"
        result = fetch_page(url)
        delay = time.time() - start_time
        # response_time = response.elapsed.total_seconds()
        html = result[0]
        status = result[1]
        size = result[2]

        print(f"La page {i} contient {len(html)} caractères")
        page_name = f"page{i}.html"
        create_html_page(page_name, html)

        data.append({
            'URL de la page' : url,
            'Statut HTTP' : status,
            'Taille en octets' : size,
            'Temps de réponse' : delay
        })
        time.sleep(1)

    df = pd.DataFrame(data)
    print(f"df : \n {df}")
    create_report(df)



def create_report(df):
    logger.info("===== CREATION RAPPORT CSV : =====")
    df.to_csv('output/csv/report.csv', sep=' ', index=False)

def create_html_page(page_name, html):
    logger.info("===== CREATION PAGES HTML : =====")
    with open(f"output/html/{page_name}", 'w', encoding="utf-8") as f:
        f.write(html)

if __name__ == '__main__':
    main()

