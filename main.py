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

# Scraper l'auteur (assumer que l'auteur est trouvé ici)
auteur_tag = soup.find('a', href=lambda href: href and 'mpanoratra' in href)
auteur = auteur_tag.text.strip() if auteur_tag else "AORN"  # Valeur par défaut à "AORN"

# Scraper le contenu du poème
contenu_div = soup.find('div', class_='col-md-8')
lines = contenu_div.get_text().splitlines()

# Filtrer les lignes non vides
contenu_poeme = [line.strip() for line in lines if line.strip()]

# Diviser le contenu en strophes (en fonction des sauts de ligne et du début des nouvelles strophes)
strophes = []
current_strophe = []

# Logique pour diviser les strophes sans inclure d'éléments comme "Midira aloha" ou d'autres éléments parasites
for line in contenu_poeme:
    if line.startswith("Hianoka") and current_strophe:  # Identifier les nouvelles strophes
        strophes.append(current_strophe)
        current_strophe = []
    if "Midira aloha" not in line:  # Éliminer les lignes incorrectes
        current_strophe.append(line)

# Ajouter la dernière strophe si non vide
if current_strophe:
    strophes.append(current_strophe)

# Construire le dictionnaire du poème
poeme_dict = {
    "titre": titre,
    "auteur": auteur,
    "contenu": [{"strophe": i+1, "texte": strophe} for i, strophe in enumerate(strophes)]
}

# Convertir le dictionnaire en JSON
poeme_json = json.dumps(poeme_dict, indent=4, ensure_ascii=False)

# Afficher le JSON
print(poeme_json)
