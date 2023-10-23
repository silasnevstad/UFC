from sources.api.api_client import APIClient
import urllib
import urllib.request
import xml.etree.ElementTree as ET

class ArxivClient(APIClient):
    BASE_URL = 'http://export.arxiv.org/api/query'

    def search(self, query):
        params = {
            'search_query': query,
            'start': 0,
            'max_results': 5
        }
        url = self.BASE_URL + '?' + urllib.parse.urlencode(params)
        data = urllib.request.urlopen(url)
        xml_response = data.read().decode('utf-8')
        return self.process_arxiv_response(xml_response)

    def retrieve_item(self, item_id):
        url = f'{self.BASE_URL}?id_list={item_id}'
        data = urllib.request.urlopen(url)
        xml_response = data.read().decode('utf-8')
        return self.process_arxiv_response(xml_response)

    def process_arxiv_response(self, xml_response):
        root = ET.fromstring(xml_response)
        search_results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            url = entry.find('{http://www.w3.org/2005/Atom}id').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
            search_results.append({
                'title': title,
                'url': url,
                'summary': summary,
                'authors': authors
            })
        return search_results[:5]

    def get_metadata(self, item_id):
        item_data = self.retrieve_item(item_id)
        return item_data[0] if item_data else None