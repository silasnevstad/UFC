from sources.web.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup

class BBCScraper(WebScraper):
    BASE_URL = 'https://www.bbc.co.uk/search'

    def search(self, query):
        params = {
            'q': query,
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []
        return self.parse_search_results(response.content)

    def parse_search_results(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('div', {"data-testid": "default-promo"})
        articles = []
        for result in search_results[:5]:  # Limiting to the first 5 results
            title_tag = result.find('p', class_='ssrcss-6arcww-PromoHeadline')
            if title_tag:
                title_tag = title_tag.find('span', {"aria-hidden": "false"})
                if title_tag:
                    title = title_tag.text
                    a_tag = result.find('a', class_='ssrcss-its5xf-PromoLink')
                    if a_tag:
                        url = a_tag['href']
                        text_content = self.retrieve_page(url)
                        articles.append({
                            'title': title,
                            'url': url,
                            'text': text_content
                        })
        return articles