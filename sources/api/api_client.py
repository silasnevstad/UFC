from sources.client import BaseClient
import requests

class APIClient(BaseClient):
    def __init__(self):
        super().__init__()

    def search(self, query):
        raise NotImplementedError

    def retrieve_item(self, item_id):
        raise NotImplementedError

    def get_metadata(self, item_id):
        raise NotImplementedError