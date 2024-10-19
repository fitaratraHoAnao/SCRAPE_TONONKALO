import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/lyrics', methods=['GET'])
def get_lyrics():
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
        # Chercher le div qui contient les paroles
        lyrics_div = soup.find_all('div', class_='print my-3 fst-italic')[0]  
        
        for line in lyrics_div.find_all_next(text=True):
            # On ajoute uniquement des lignes de texte qui ne sont pas vides
            if line.strip() and line not in lyrics:
                lyrics.append(line.strip())

        # Extraire l'auteur et la date
        footer = lyrics_div.find_all_next('div')
        author = footer[-1].text.strip() if footer else "Auteur introuvable"
        date = "03 MAI 2024"  # Date statique

        # Créer le dictionnaire
        data = {
            "title": title,
            "lyrics": lyrics,
            "author": author,
            "date": date
        }

        return jsonify(data)
    else:
        return jsonify({"error": f"Erreur lors du scraping : {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
