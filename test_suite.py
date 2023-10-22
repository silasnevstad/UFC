import unittest

# Import the test modules
from sources.web.web_tests import *
from sources.api.api_tests import *

def create_test_suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    # test_suite.addTest(loader.loadTestsFromTestCase(TestReutersScraper)) # WIP - requires selenium
    # test_suite.addTest(loader.loadTestsFromTestCase(TestNPRScraper)) # WIP - requires selenium
    test_suite.addTest(loader.loadTestsFromTestCase(TestNewsAPIClient))
    test_suite.addTest(loader.loadTestsFromTestCase(TestNatureScraper))
    test_suite.addTest(loader.loadTestsFromTestCase(TestArxivClient))
    test_suite.addTest(loader.loadTestsFromTestCase(TestPubMedClient))
    test_suite.addTest(loader.loadTestsFromTestCase(TestDPLAClient))
    test_suite.addTest(loader.loadTestsFromTestCase(TestGoogleScholarScraper))
    test_suite.addTest(loader.loadTestsFromTestCase(TestNationalArchivesScraper))
    test_suite.addTest(loader.loadTestsFromTestCase(TestHistoryNetScraper))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBBCScraper))
    
    return test_suite

if __name__ == "__main__":
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(create_test_suite())