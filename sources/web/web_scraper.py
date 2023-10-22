import requests
from bs4 import BeautifulSoup
from readability.readability import Document
import fitz
import tempfile
import os

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        })

    def search(self, query):
        raise NotImplementedError

    def retrieve_page(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {str(e)}")
            return ''
        
        content_type = response.headers.get('Content-Type')
        if 'text/html' in content_type:
            return self.parse_page_content(response.content)
        elif 'application/pdf' in content_type:
            return self.parse_pdf_content(response.content)
        else:
            print(f"Unhandled content type {content_type} for URL {url}")
            return ''

    def parse_page(self, html_content):
        raise NotImplementedError
    
    def parse_page_content(self, html_content):
        doc = Document(html_content)
        cleaned_html = doc.summary()
        
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content
    
    def parse_pdf_content(self, pdf_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name

        pdf_stream = fitz.open(temp_file_path)

        text = ''
        for page in pdf_stream:
            text += page.get_text()

        pdf_stream.close()
        os.unlink(temp_file_path)

        return text