import pdfplumber
import os
from pathlib import Path

def search_pdf_for_keywords(pdf_path, keywords):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            found_keywords = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    for keyword in keywords:
                        if keyword.lower() in text.lower() and keyword not in found_keywords:
                            found_keywords.append(keyword)
            return found_keywords
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return []

def scan_pdfs_in_directory(directory, keywords):
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"Directory {directory} does not exist.")
        return

    for pdf_file in directory_path.glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")
        found = search_pdf_for_keywords(pdf_file, keywords)
        if found:
            print(f"Found keywords: {', '.join(found)}")
        else:
            print("No keywords found.")

if __name__ == "__main__":
    # Specify the directory containing PDF files
    pdf_directory = r"D:\Documents"  # Directory path, not a file
    # List of keywords to search for
    keywords = ["General Questions about MDSAP", "Questions related to Assessments", "Questions related to Audits"]
    
    scan_pdfs_in_directory(pdf_directory, keywords)