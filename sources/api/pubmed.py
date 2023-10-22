from sources.api.api_client import APIClient
import requests
from decouple import config
from xml.etree import ElementTree

class PubMedClient(APIClient):
    BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    FETCH_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    def __init__(self, api_key=None):
        self.api_key = api_key or config('PUBMED_API_KEY')

    def search(self, query):
        params = {
            'db': 'pubmed',
            'term': query,
            'api_key': self.api_key,
            'retmode': 'xml',
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []
        return self.process_pubmed_response(response.content)

    def retrieve_item(self, pmid):
        params = {
            'db': 'pubmed',
            'id': pmid,
            'api_key': self.api_key,
            'retmode': 'xml',
        }
        response = requests.get(self.FETCH_URL, params=params)
        if response.status_code != 200:
            return {}
        return self.parse_item_response(response.content)

    def process_pubmed_response(self, xml_content):
        tree = ElementTree.fromstring(xml_content)
        article_ids = [id_elem.text for id_elem in tree.findall('.//Id')]
        articles = []
        for article_id in article_ids:
            article_data = self.retrieve_item(article_id)
            if article_data:
                articles.append(article_data)
        return articles[:5]  # Limiting to the first 5 articles

    def parse_item_response(self, xml_content):
        tree = ElementTree.fromstring(xml_content)
        abstract_text = ""
        for abstract in tree.findall('.//AbstractText'):
            abstract_text += abstract.text + " "
        article_data = {
            'title': tree.findtext('.//ArticleTitle'),
            'url': f'https://pubmed.ncbi.nlm.nih.gov/{tree.findtext(".//PMID")}/',
            'text': abstract_text,
        }
        return article_data

    def get_metadata(self, pmid):
        item_data = self.retrieve_item(pmid)
        return item_data 