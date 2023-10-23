from sources.client import BaseClient
import requests

class WebScraper(BaseClient):
    def __init__(self):
        super().__init__()

    def search(self, query):
        raise NotImplementedError