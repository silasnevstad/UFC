from sources.web.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup

class HistoryNetScraper(WebScraper):
    BASE_URL = 'https://www.historynet.com/'

    def search(self, query):
        params = {
            's': query,
        }
        response = self.session.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve HistoryNet search results: {response.status_code}")
            return []
        return self.parse_search_results(response.content, query)
    
    def parse_search_results(self, html_content, query):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('article')
        articles = []
        for result in search_results[:5]:  # Limiting to the first 5 results
            title_tag = result.find('h2', class_='entry-title').find('a')
            if title_tag:  # Ensure title_tag is not None
                title = title_tag.text
                url = title_tag['href']
                text_content = self.retrieve_page(url, query)
                articles.append({
                    'title': title,
                    'url': url,
                    'text': text_content
                })
        return articles