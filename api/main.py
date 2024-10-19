import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scrape')
def scrape():
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
        lyrics_div = soup.find_all('div', class_='print my-3 fst-italic')[0]
        for line in lyrics_div.find_next_siblings(text=True):
            if line.strip():
                lyrics.append(line.strip())

        # Extraire l'auteur
        footer = lyrics_div.find_all_next('div')
        author = footer[-1].text.strip() if footer else "Auteur introuvable"

        # Date statique
        date = "03 MAI 2024"

        # Créer le dictionnaire
        data = {
            "title": title,
            "lyrics": lyrics,
            "author": author,
            "date": date
        }

        # Retourner le résultat en JSON
        return jsonify(data)
    else:
        return jsonify({"error": f"Erreur lors du scraping : {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
