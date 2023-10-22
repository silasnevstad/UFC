from sources.web.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup

class NationalArchivesScraper(WebScraper):
    BASE_URL = 'https://search.archives.gov/search'

    def search(self, query):
        params = {
            'query': query,
            'submit': '',
            'utf8': '',
            'affiliate': 'national-archives'
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []
        return self.parse_search_results(response.content, query)

    def parse_search_results(self, html_content, query):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('div', class_='content-block-item result')
        articles = []
        for result in search_results[:5]:  # Limiting to the first 5 results
            title_tag = result.find('h4', class_='title').find('a')
            title = title_tag.text
            url = title_tag['href']
            text_content = self.retrieve_page(url, query)
            articles.append({
                'title': title,
                'url': url,
                'text': text_content
            })
        return articles

        