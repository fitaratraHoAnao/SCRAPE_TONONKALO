from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def recherche():
    auteur = request.args.get('auteur')
    titre = request.args.get('titre')

    # URL de la page à scraper (remplacez ceci par l'URL dynamique basée sur l'auteur et le titre)
    url = f'https://vetso.serasera.org/tononkalo/{auteur}/{titre}'

    try:
        # Envoyer une requête HTTP pour obtenir le contenu de la page
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs de requête

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scraper le titre
        titre_page = soup.find('h2').text.strip()

        # Scraper le contenu du poème
        contenu_div = soup.find('div', class_='col-md-8')
        lines = contenu_div.get_text().splitlines()

        # Filtrer les lignes non vides et supprimer les éléments indésirables
        elements_a_supprimer = [
            "Rohy:", 
            "Adikao", 
            "Sokajy :", 
            "Mpakafy:", 
            "Hametraka hevitra", 
            "Midira aloha", 
            "rina15", 
            "Fitiavana", 
            "108                        1",
            "HIANOKA ! (AORN)",  # Ligne à supprimer
            "Mbola tsisy niantsa",
            "Hangataka antsa",
            "(Nalaina tao amin'ny vetso.serasera.org)"
        ]

        # Filtrer le contenu
        contenu_poeme = [line.strip() for line in lines if line.strip() and not any(el in line for el in elements_a_supprimer)]

        # Construire le texte du poème en une seule chaîne
        tononkalo_text = ',\n'.join(contenu_poeme)  # Utilise une virgule pour séparer les lignes

        # Construire la réponse JSON
        poeme_dict = {
            "Tononkalo": tononkalo_text,
            "titre": titre_page
        }

        return jsonify(poeme_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
