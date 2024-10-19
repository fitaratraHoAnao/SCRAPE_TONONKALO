import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = "https://vetso.serasera.org/tononkalo/aorn/hianoka"

# Faire la requête GET
response = requests.get(url)

# Vérifier que la requête a réussi
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraire le titre
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "Titre introuvable"
    
    # Extraire les paroles
    lyrics = []
    lyrics_div = soup.find('div', class_='print my-3 fst-italic')  # Correction de la recherche
    if lyrics_div:
        # Obtenir le texte brut en enlevant les balises HTML
        lyrics_text = lyrics_div.find_next_sibling(text=True).strip()
        lyrics = [line.strip() for line in lyrics_text.split('\n') if line.strip()]  # Nettoyage des lignes

    # Extraire l'auteur et la date
    footer = lyrics_div.find_next('div').find_all('div')
    author = footer[-1].text.strip() if footer else "Auteur introuvable"
    date = "03 MAI 2024"  # Date statique

    # Créer le dictionnaire
    data = {
        "title": title,
        "lyrics": lyrics,
        "author": author,
        "date": date
    }

    # Afficher le résultat en JSON
    json_output = json.dumps(data, ensure_ascii=False, indent=2)
    print(json_output)
else:
    print(f"Erreur lors du scraping : {response.status_code}")
