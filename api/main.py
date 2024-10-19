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
        lyrics = [line.strip() for line in lyrics_div.find_all_next(string=True) if line.strip() and line != "--------"]

        # Extraire l'auteur et la date à partir du texte
        author_date_div = lyrics_div.find_next_sibling(text=True).strip().split('<br />')
        lyrics += [line.strip() for line in author_date_div if line.strip()]

        # Extraire l'auteur et la date
        date = lyrics[-1] if lyrics else "Date introuvable"
        author = lyrics[-2] if len(lyrics) > 1 else "Auteur introuvable"

        # Créer le dictionnaire
        data = {
            "title": title,
            "lyrics": lyrics[:-2],  # Exclure l'auteur et la date des paroles
            "author": author,
            "date": date
        }

        return jsonify(data)
    else:
        return jsonify({"error": "Erreur lors du scraping"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
