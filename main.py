import requests
from bs4 import BeautifulSoup

def scrape_quotes(url):
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all quote containers
        quotes = soup.find_all('div', class_='quote')

        for idx, quote in enumerate(quotes, start=1):
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            print(f"{idx}. \"{text}\" — {author}")

    except requests.RequestException as e:
        print("Request failed:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    url = "https://quotes.toscrape.com"
    scrape_quotes(url)
