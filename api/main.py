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
    if title_element:
        title = title_element.get_text(strip=True).replace("(", "").replace(")", "")
    else:
        title = "Title not found"

    # Extract the poem's content
    poem = ""
    poem_block = title_element.find_next("div")
    if poem_block:
        poem = poem_block.get_text(separator="\n", strip=True)
    
    # Extract the author's name and date
    author_element = soup.find('a', class_='text-decoration-none')
    if author_element:
        author = author_element.get_text(strip=True)
    else:
        author = "Author not found"

    date_element = soup.find(text='03 MAI 2024')
    date = date_element.strip() if date_element else "Date not found"

    # Prepare data as JSON
    result = {
        "title": title,
        "author": author,
        "poem": poem.splitlines(),
        "date": date
    }

    # Return the JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
