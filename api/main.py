import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def scrape_and_return_json():
    # URL to scrape
    url = "https://vetso.serasera.org/tononkalo/aorn/hianoka"

    # Send a GET request to fetch the page
    response = requests.get(url)
    
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the poem's title and author
    title_element = soup.find('h2', class_='border-bottom')
    title = title_element.get_text(strip=True).replace("(", "").replace(")", "")

    # Extract the poem's content
    poem = title_element.find_next_sibling(text=True, recursive=False).strip()

    # Extract the rest of the poem by navigating through the sibling elements
    poem_lines = poem.splitlines()
    
    # Additional lines follow under the next <br /> tags, extract them
    poem_lines += [line.strip() for line in title_element.find_next_siblings(text=True) if line.strip()]
    
    # Extract the author's name and date
    author = soup.find('a', class_='text-decoration-none').get_text(strip=True)
    date = soup.find(text='03 MAI 2024').strip()

    # Prepare data as JSON
    result = {
        "title": title,
        "author": author,
        "poem": poem_lines,
        "date": date
    }

    # Return the JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
