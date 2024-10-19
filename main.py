from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def search_lyrics():
    tononkalo = request.args.get('tononkalo')
    author = request.args.get('author')

    if not tononkalo or not author:
        return jsonify({"error": "Veuillez fournir tononkalo et author"}), 400

    url = f"https://vetso.serasera.org/tononkalo/{author}/{tononkalo.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire le titre
        title_tag = soup.find('h2')
        title = title_tag.text.strip() if title_tag else "Titre introuvable"

        # Extraire les paroles
        lyrics_div = soup.find('div', class_='print my-3 fst-italic')
        lyrics_lines = [line.strip() for line in lyrics_div.stripped_strings]

        # Récupérer la date et l'auteur en vérifiant les derniers éléments
        if len(lyrics_lines) >= 2:
            date = lyrics_lines[-1]  # Dernier élément
            author = lyrics_lines[-2]  # Avant-dernier élément
            lyrics = lyrics_lines[:-2]  # Les autres éléments comme paroles
        else:
            return jsonify({"error": "Informations manquantes"}), 404

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
