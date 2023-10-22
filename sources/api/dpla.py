from sources.api.api_client import APIClient
import requests
from decouple import config

class DPLAClient(APIClient):
    BASE_URL = 'https://api.dp.la/v2/items'

    def __init__(self, api_key=None):
        self.api_key = api_key or config('DPLA_API_KEY')

    def search(self, query):
        params = {
            'q': query,
            'api_key': self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return self.process_dpla_response(response.json())

    def retrieve_item(self, item_id):
        url = f'{self.BASE_URL}/{item_id}'
        params = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def process_dpla_response(self, response):
        documents = response['docs']
        search_results = []
        for doc in documents:
            title = ', '.join(doc['sourceResource'].get('title', []))
            url = doc.get('isShownAt', '')
            page_content = ' '.join(doc['sourceResource'].get('description', [])) + \
                        ' '.join(doc['sourceResource'].get('creator', []))
            search_results.append({
                'title': title,
                'url': url,
                'page_content': page_content
            })
        return search_results[:5]

    def get_metadata(self, item_id):
        item_data = self.retrieve_item(item_id)
        return item_data.get('metadata', {})