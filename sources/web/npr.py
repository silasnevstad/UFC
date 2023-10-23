from sources.web.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup

class NPRScraper(WebScraper):
    BASE_URL = 'https://www.npr.org/search/'

    def search(self, query):
        params = {
            'query': query,
            'page': 1,
            'sortType': 'bestMatch'
        }
        response = self.session.get(self.BASE_URL, params=params)
        print("RESPONSE TEXT: ", response.text)
        if response.status_code != 200:
            return []
        return self.parse_search_results(response.content, query)

    def parse_search_results(self, html_content, query):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('li', class_='ais-InfiniteHits-item')
        articles = []
        for result in search_results[:5]:  # Limiting to the first 5 results
            title_tag = result.find('h2', class_='title').find('a')
            title = title_tag.text
            url = title_tag['href']
            if url.startswith('/'):
                url = 'https://www.npr.org' + url
            text_content = self.retrieve_page(url, query)
            if text_content == '':
                continue
            articles.append({
                'title': title,
                'url': url,
                'text': text_content
            })
        return articles

        