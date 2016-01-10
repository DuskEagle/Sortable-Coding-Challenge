import sys
import unittest

sys.path.append('../src')

from Product import Product
from ProductListingMatcher import ProductListingMatcher

class RegexMatchingTest(unittest.TestCase):
    
    def __testListingMatched(self, product, listing, should_match=True):
        """ Helper method for the tests. We test if listing is found as a match
        for product. If should_match == False, we instead check that listing
        is not found as a match for product."""
        self.matcher = ProductListingMatcher("", "", "")
        self.matcher._ProductListingMatcher__loadProducts([product])
        self.matcher._ProductListingMatcher__matchListings([listing])
        product, = list(filter(lambda x: len(x) != 0, self.matcher._ProductListingMatcher__product_dict.values()))[0]
        listing_results = self.matcher._ProductListingMatcher__product_listing_dict[product]
        if should_match:
            self.assertEqual(len(listing_results), 1)
        else:
            self.assertEqual(len(listing_results), 0)
    
    def testBasic(self):
        product = """{"model":"QV-3000EX","manufacturer":"Casio","product_name":"","announced-date":"2000-01-03T19:00:00.000-05:00"}"""
        listing = """{"title":"Casio QV-3000EX","manufacturer":"Casio","currency":"CAD","price":"0.00"}"""
        self.__testListingMatched(product, listing)
    
    def testBrackets(self):
        product = """{"model":"QV-3000(EX)","manufacturer":"Casio","product_name":"","announced-date":"2000-01-03T19:00:00.000-05:00"}"""
        listing = """{"title":"Casio QV-3000(EX)","manufacturer":"Casio","currency":"CAD","price":"0.00"}"""
        self.__testListingMatched(product, listing)

    def testDifferingUpperAndLowerCase(self):
        product = """{"model":"QV-3000EX","manufacturer":"Casio","product_name":"","announced-date":"2000-01-03T19:00:00.000-05:00"}"""
        listing = """{"title":"Casio Qv-3000ex","manufacturer":"Casio","currency":"CAD","price":"0.00"}"""
        self.__testListingMatched(product, listing)
        
    def testWhitespaceAndHyphens(self):
        product = """{"model":"QV 3000EX","manufacturer":"Casio","product_name":"","announced-date":"2000-01-03T19:00:00.000-05:00"}"""
        listing = """{"title":"Casio Q V 3000-EX","manufacturer":"Casio","currency":"CAD","price":"0.00"}"""
        self.__testListingMatched(product, listing)
        
    def testNextWordNotConfusedWithPartOfModelName(self):
        product = """{"model":"QV 3000EX","manufacturer":"Casio","product_name":"","announced-date":"2000-01-03T19:00:00.000-05:00"}"""
        listing = """{"title":"Casio QV-3000 Extra Special Dealz","manufacturer":"Casio","currency":"CAD","price":"0.00"}"""
        self.__testListingMatched(product, listing, should_match=False)
