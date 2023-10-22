import unittest
import time
from sources.api.dpla import DPLAClient
from sources.api.arxiv import ArxivClient
from sources.api.pubmed import PubMedClient

class TimedTestCase(unittest.TestCase):
    def time_method(self, method, *args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'{self.__class__.__name__}.{method.__name__} took {elapsed_time:.2f} seconds')
        return result

class TestDPLAClient(TimedTestCase):
    def setUp(self):
        self.client = DPLAClient()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.client.search, query)
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)

class TestArxivClient(TimedTestCase):
    def setUp(self):
        self.client = ArxivClient()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.client.search, query)
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)

class TestPubMedClient(TimedTestCase):
    def setUp(self):
        self.client = PubMedClient()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.client.search, query)
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)