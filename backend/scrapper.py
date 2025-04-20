import requests
from bs4 import BeautifulSoup
import logging
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape(URL: str ='https://www.geeksforgeeks.org/python-programming-language/'):
    try:
        logging.info(f"Scrapping {URL}")
        if not URL:
            logging.warning("Missing URL.")
            return jsonify({"error": "Missing URL"}), 400
        
        # Making a GET request
        r = requests.get(URL)

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        text = soup.get_text()

        # s = soup.find('div', class_='entry-content')
        # content = soup.find_all('p')
        # print(content)
        logging.info(f"Returning content.")

        return text
    
    except Exception as e:
        logging.exception("Unexpected error in scraping.")
        return jsonify({"error": "Internal server error"}), 500
    

if __name__ == '__main__':
    scrape('https://www.geeksforgeeks.org/python-web-scraping-tutorial/')