import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = 'https://vetso.serasera.org/tononkalo/aorn/hianoka'

# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Scraper le titre
titre = soup.find('h2').text.strip()

# Scraper l'auteur
auteur_tag = soup.find('a', href=lambda href: href and 'mpanoratra' in href)
auteur = auteur_tag.text.strip() if auteur_tag else "Inconnu"

# Scraper la date (dans ce cas, la date est dans la dernière ligne du poème)
contenu_div = soup.find('div', class_='col-md-8')
lines = contenu_div.get_text().splitlines()

# Récupérer les lignes non vides (correspondant aux strophes)
contenu_poeme = [line.strip() for line in lines if line.strip()]
date = contenu_poeme[-1]  # La date semble être à la fin du poème

# Diviser le contenu en strophes
strophes = []
current_strophe = []

for line in contenu_poeme:
    if line.startswith("Hianoka") and current_strophe:  # nouvelle strophe
        strophes.append(current_strophe)
        current_strophe = []
    current_strophe.append(line)

# Ajouter la dernière strophe
if current_strophe:
    strophes.append(current_strophe)

# Construire le dictionnaire du poème
poeme_dict = {
    "titre": titre,
    "auteur": auteur,
    "date": date,
    "contenu": [{"strophe": i+1, "texte": strophe} for i, strophe in enumerate(strophes)]
}

# Convertir le dictionnaire en JSON
poeme_json = json.dumps(poeme_dict, indent=4, ensure_ascii=False)

# Afficher le JSON
print(poeme_json)
