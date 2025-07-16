import requests
import fitz  

def download_pdf(url, filename='download.pdf'):
    response = requests.get(url)
    response.raise_for_status()  
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"PDF downloaded: {filename}")
    return filename

def extract_text_from_pdf(filename):
    doc = fitz.open(filename)
    text = ""
    for page_num, page in enumerate(doc, start=1):
        text += f"\n--- Page {page_num} ---\n"
        text += page.get_text()
    doc.close()
    return text

if __name__ == "__main__":
    
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    pdf_file = download_pdf(pdf_url)
    content = extract_text_from_pdf(pdf_file)
    
    print("\n--- Extracted Text ---\n")
    print(content)
