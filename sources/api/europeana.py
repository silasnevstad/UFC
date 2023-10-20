from sources.api.api_client import APIClient
import requests

class EuropeanaClient(APIClient):
    BASE_URL = 'https://api.europeana.eu/record/v2/search.json'

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        params = {
            'query': query,
            'wskey': self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()  # This assumes the response is JSON formatted

    def retrieve_item(self, item_id):
        # Assume item retrieval is part of the search endpoint (this may vary)
        return self.search('europeana_id:"{}"'.format(item_id))

    def get_metadata(self, item_id):
        # Assume metadata retrieval is part of item retrieval (this may vary)
        item_data = self.retrieve_item(item_id)
        return item_data.get('metadata', {})