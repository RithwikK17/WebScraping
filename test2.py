import requests
from bs4 import BeautifulSoup

def scrape_books(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        for idx, book in enumerate(books, start=1):
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            print(f"{idx}. {title} — {price}")

    except requests.RequestException as e:
        print("Request failed:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    url = "https://books.toscrape.com"
    scrape_books(url)
