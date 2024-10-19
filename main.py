from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    url = "https://vetso.serasera.org/tononkalo/aorn/hianoka"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire le titre
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Titre introuvable"
        
        # Extraire les paroles
        lyrics_div = soup.find_all('div', class_='print my-3 fst-italic')[0]  # Correction ici
        lyrics = [line.strip() for line in lyrics_div.find_all_next(text=True) if line.strip()]
        
        # Extraire l'auteur
        author_tag = soup.find('div', class_='print my-3 fst-italic')
        author = "AORN"  # Utiliser une valeur statique ici, ou extraire dynamiquement si disponible
        
        # Date statique
        date = "03 MAI 2024"

        # Créer le dictionnaire
        data = {
            "title": title,
            "lyrics": lyrics,
            "author": author,
            "date": date
        }

        return jsonify(data)
    else:
        return jsonify({"error": "Erreur lors du scraping"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
