import requests
from bs4 import BeautifulSoup
from readability.readability import Document
import fitz
import tempfile
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

class BaseClient:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        })

    def search(self, query):
        raise NotImplementedError

    def retrieve_page(self, url, query):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {str(e)}")
            return ''

        content_type = response.headers.get('Content-Type')
        if 'text/html' in content_type:
            return self.parse_page_content(response.content, query)
        elif 'application/pdf' in content_type:
            return self.parse_pdf_content(response.content)
        else:
            print(f"Unhandled content type {content_type} for URL {url}")
            return ''

    def parse_page_content(self, html_content, query):
        doc = Document(html_content)
        cleaned_html = doc.summary()

        soup = BeautifulSoup(cleaned_html, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)

        text_content = text_content.replace('\\"', '').replace('\\', '').replace('\"', '').replace('\'', '').replace('\n', '').replace('\xa0', '')

        if text_content == '':
            return ''

        return self.extract_relevant_sentences(text_content, query)

    def parse_pdf_content(self, pdf_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name

        try:
            pdf_stream = fitz.open(temp_file_path)
        except:
            print(f"Failed to open PDF file {temp_file_path}")
            return ''

        text = ''
        for page in pdf_stream:
            text += page.get_text()

        pdf_stream.close()
        os.unlink(temp_file_path)

        return text

    def extract_relevant_sentences(self, text_content, query):
        # Remove boilerplate and other irrelevant content
        text_content = text_content.replace("Loading\nSomething is loading.", "")
        
        doc = self.nlp(text_content)
        sentences = [sent.text for sent in doc.sents]
        
        query_entities = [ent.text for ent in self.nlp(query).ents]
        
        entity_boosted_sentences = [sent.text for sent in doc.sents if any(entity in sent.text for entity in query_entities)]
        
        corpus = sentences + entity_boosted_sentences + [query]
        
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        vectors = vectorizer.toarray()
        
        cosine_similarities = cosine_similarity(vectors[-1].reshape(1, -1), vectors[:-1]).flatten()
        
        # Use a threshold or dynamically determine number of sentences to retrieve
        threshold = 0.1
        relevant_indices = [i for i, score in enumerate(cosine_similarities) if score > threshold]
        
        # Get adjacent sentences for context
        extended_indices = set()
        for i in relevant_indices:
            extended_indices.add(i)
            if i > 0:
                extended_indices.add(i-1)
            if i < len(sentences) - 1:
                extended_indices.add(i+1)
        
        relevant_sentences = []
        for i in sorted(extended_indices):
            try:
                relevant_sentences.append(sentences[i])
            except IndexError:
                pass
        
        return ' '.join(relevant_sentences)