import unittest
import time
from sources.web.national_archives import NationalArchivesScraper
from sources.web.history_net import HistoryNetScraper
from sources.web.bbc import BBCScraper
from sources.web.google_scholar import GoogleScholarScraper
from sources.web.reuters import ReutersScraper
from sources.web.nature import NatureScraper

class TimedTestCase(unittest.TestCase):
    def time_method(self, method, *args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'{self.__class__.__name__}.{method.__name__} took {elapsed_time:.2f} seconds')
        return result

class TestNationalArchivesScraper(TimedTestCase):
    def setUp(self):
        self.scraper = NationalArchivesScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

class TestHistoryNetScraper(TimedTestCase):
    def setUp(self):
        self.scraper = HistoryNetScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

class TestBBCScraper(TimedTestCase):
    def setUp(self):
        self.scraper = BBCScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

class TestGoogleScholarScraper(TimedTestCase):
    def setUp(self):
        self.scraper = GoogleScholarScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

class TestReutersScraper(TimedTestCase):
    def setUp(self):
        self.scraper = ReutersScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

class TestNatureScraper(TimedTestCase):
    def setUp(self):
        self.scraper = NatureScraper()

    def test_search(self):
        query = 'test'
        results = self.time_method(self.scraper.search, query)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)