from sources.web.web_scraper import WebScraper
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class ReutersScraper(WebScraper):
    BASE_URL = 'https://www.reuters.com/site-search/'

    def __init__(self):
        self.session = HTMLSession()

    def search(self, query):
        params = {
            'query': query,
            'sort': 'newest',
        }
        response = self.session.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []
        response.html.render()  # This line executes JavaScript
        print(response.html.raw_html)
        return self.parse_search_results(response.html.raw_html, query)

    def parse_search_results(self, html_content, query):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('div', class_='media-story-card__body__3tRWy')
        articles = []
        for result in search_results[:5]:  # Limiting to the first 5 results
            title_tag = result.find('h3', class_='text__text__1FZLe')
            if title_tag:
                title = title_tag.text.strip()
                url_tag = title_tag.find('a')
                if url_tag:
                    url = url_tag['href']
                    if url.startswith('/'):
                        url = 'https://www.reuters.com' + url
                    text_content = self.retrieve_page(url, query)
                    articles.append({
                        'title': title,
                        'url': url,
                        'text': text_content
                    })
        return articles