from sources.api.api_client import APIClient
from newsapi import NewsApiClient
from decouple import config
import requests

class NewsAPIClient(APIClient):
    BASE_URL = 'https://newsapi.org/v2/everything'

    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key or config('NEWSAPI_API_KEY')
        self.newsapi = NewsApiClient(api_key=self.api_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        })

    def search(self, query):
        response = self.newsapi.get_everything(
            q=query,
            sources='bbc-news,reuters,the-new-york-times,associated-press,bloomberg,cnn,the-washington-post,business-insider,medical-news-today,national-geographic,new-scientist',
            language='en',
            sort_by='relevancy',
            page=1)
        return self.process_newsapi_response(response, query)

    def process_newsapi_response(self, response, query):
        articles = response["articles"]
        search_results = []
        for article in articles[:5]:
            title = article["title"]
            url = article["url"]
            description = article["description"]
            content = article["content"]
            source = article["source"]["name"]
            full_text = self.retrieve_page(url, query)
            search_results.append({
                'title': title,
                'url': url,
                'text': full_text,
                'source': source
            })
        return search_results