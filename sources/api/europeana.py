from sources.api.api_client import APIClient
import requests
from decouple import config

class EuropeanaClient(APIClient):
    BASE_URL = 'https://api.europeana.eu/record/v2/search.json'

    def __init__(self, api_key=None):
        self.api_key = api_key or config('EUROPEANA_API_KEY')

    def search(self, query):
        params = {
            'query': query,
            'wskey': self.api_key,
            'rows': 5,
            'MEDIA': 'true',
            'MIME_TYPE': 'text/html',
        }
        response = requests.get(self.BASE_URL, params=params)
        response_json = response.json()  # This assumes the response is JSON formatted
        
        if response_json.get("success"):
            items = response_json.get("items", [])
            result_list = []
            for item in items:
                title = item.get('title', ["No title available"])[0]  # Assuming title is a list
                url = item.get('guid')  # Modify this if the URL is located elsewhere
                description = item.get('dcDescription', ["No description available"])[0]  # Assuming dcDescription is a list
                
                result_list.append({
                    'title': title,
                    'url': url,
                    'text': description
                })
            return result_list
        else:
            print(f"Failed to retrieve data: {response_json.get('error')}")
            return []  # This assumes the response is JSON formatted

    def retrieve_item(self, item_id):
        # Assume item retrieval is part of the search endpoint (this may vary)
        return self.search('europeana_id:"{}"'.format(item_id))

    def get_metadata(self, item_id):
        # Assume metadata retrieval is part of item retrieval (this may vary)
        item_data = self.retrieve_item(item_id)
        return item_data.get('metadata', {})