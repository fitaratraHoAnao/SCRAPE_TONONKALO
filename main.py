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

# Scraper le contenu du poème
contenu_div = soup.find('div', class_='col-md-8')
lines = contenu_div.get_text().splitlines()

# Filtrer les lignes non vides et supprimer les éléments indésirables
elements_a_supprimer = ["Rohy:", "Adikao", "Sokajy :", "Mpakafy:", "Hametraka hevitra", "Midira aloha", "rina15"]
contenu_poeme = [line.strip() for line in lines if line.strip() and not any(el in line for el in elements_a_supprimer)]

# Diviser le contenu en strophes (en fonction des sauts de ligne et du début des nouvelles strophes)
strophes = []
current_strophe = []

# Logique pour diviser les strophes
for line in contenu_poeme:
    if line.startswith("Hianoka") and current_strophe:  # Identifier les nouvelles strophes
        strophes.append(current_strophe)
        current_strophe = []
    current_strophe.append(line)

# Ajouter la dernière strophe si non vide
if current_strophe:
    strophes.append(current_strophe)

# Construire le dictionnaire du poème sans "auteur"
poeme_dict = {
    "titre": titre,
    "contenu": [{"strophe": i+1, "texte": strophe} for i, strophe in enumerate(strophes)]
}

# Convertir le dictionnaire en JSON
poeme_json = json.dumps(poeme_dict, indent=4, ensure_ascii=False)

# Afficher le JSON
print(poeme_json)
