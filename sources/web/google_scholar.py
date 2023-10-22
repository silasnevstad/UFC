from sources.web.web_scraper import WebScraper
from serpapi import GoogleSearch
from decouple import config

class GoogleScholarScraper(WebScraper):
    BASE_URL = 'https://scholar.google.com/scholar'
    API_KEY = config('SERPAPI_API_KEY')

    def search(self, query):
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.API_KEY,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        return self.parse_search_results(organic_results)

    def parse_search_results(self, html_content):
        results = []

        for result in html_content:
            title = result.get('title')
            url = result.get('link')
            text_content = self.retrieve_page(url)

            results.append({
                'title': title,
                'url': url,
                'text_content': text_content
            })
        
        return results[:5]
        