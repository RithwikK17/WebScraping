import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re

def create_output_directory(directory="scraped_data"):
    """Create a directory to store scraped data if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clean_text(text):
    """Clean extracted text by removing extra whitespace and newlines."""
    return ' '.join(text.split())

def is_valid_url(url):
    """Validate URL format."""
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.match(url)

def scrape_website(url, output_dir="scraped_data"):
    """Scrape text and PDF files from a website."""
    try:
        # Validate URL
        if not is_valid_url(url):
            print("Invalid URL provided.")
            return

        # Send HTTP request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create output directory
        output_dir = create_output_directory(output_dir)
        
        # Extract and save text content
        text_content = soup.get_text(separator=' ', strip=True)
        cleaned_text = clean_text(text_content)
        
        text_file_path = os.path.join(output_dir, 'scraped_text_1.txt')
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Text content saved to {text_file_path}")

        # Find and download PDF files
        pdf_count = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.lower().endswith('.pdf'):
                pdf_url = urljoin(url, href)
                try:
                    pdf_response = requests.get(pdf_url, headers=headers)
                    pdf_response.raise_for_status()
                    
                    # Extract filename from URL or generate one
                    filename = os.path.basename(pdf_url)
                    if not filename.lower().endswith('.pdf'):
                        filename += '.pdf'
                    
                    pdf_path = os.path.join(output_dir, filename)
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                    print(f"PDF saved to {pdf_path}")
                    pdf_count += 1
                except requests.RequestException as e:
                    print(f"Failed to download PDF {pdf_url}: {e}")

        if pdf_count == 0:
            print("No PDF files found on the website.")
            
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Example usage
    website_url = input("Enter the website URL to scrape: ")
    scrape_website(website_url)

if __name__ == "__main__":
    main()