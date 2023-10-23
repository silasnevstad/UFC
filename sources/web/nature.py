from sources.web.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup

class NatureScraper(WebScraper):
    BASE_URL = 'https://www.nature.com/search'

    def search(self, query):
        params = {
            'q': query,
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []
        return self.parse_search_results(response.content, query)

    def parse_search_results(self, html_content, query):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('li', class_='app-article-list-row__item')
        articles = []
        for result in search_results[:5]:
            title_tag = result.find('h3', class_='c-card__title').find('a')
            title = title_tag.text
            url = title_tag['href']
            if url.startswith('/'):
                url = 'https://www.nature.com' + url
            text_content = self.retrieve_page(url, query)
            if text_content == '':
                continue
            articles.append({
                'title': title,
                'url': url,
                'text': text_content
            })
        return articles
