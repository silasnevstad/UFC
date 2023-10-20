class WebScraper:
    def search(self, query):
        raise NotImplementedError

    def retrieve_page(self, url):
        raise NotImplementedError

    def parse_page(self, html_content):
        raise NotImplementedError