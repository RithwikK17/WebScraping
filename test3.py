import requests
from bs4 import BeautifulSoup

def scrape_allinone(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    products = []
    cards = soup.select('div.product-wrapper')
    for card in cards:
        title = card.find('a', class_='title').get_text(strip=True)
        description = card.find('p', class_='description').get_text(strip=True)
        price = card.find('h4', class_='price').get_text(strip=True)
        stars = card.find('div', class_='ratings').find_all('span', class_='glyphicon-star')
        rating = len(stars)
        reviews = card.find('p', class_='review-count').get_text(strip=True)
        img = card.find('img')['src']

        products.append({
            'title': title,
            'description': description,
            'price': price,
            'rating': rating,
            'reviews': reviews,
            'image_url': img
        })

    return products

if __name__ == "__main__":
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    items = scrape_allinone(url)
    for i, p in enumerate(items, 1):
        print(f"{i}. {p['title']} — {p['price']} — {p['rating']} — {p['reviews']}")
