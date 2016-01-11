import sys
import unittest

sys.path.append('../src')

from ProductListingMatcher import ProductListingMatcher

class RegexMatchingTest(unittest.TestCase):
    
    def __testListingMatched(self, products, listing, should_match=True):
        """ Helper method for the tests. We test if listing is found as a match
        for one of products. If should_match == False, we instead check that
        listing is not found as a match for product."""
        
        if isinstance(products, str):
            products = [products]
        
        self.matcher = ProductListingMatcher("", "", "")
        self.matcher._ProductListingMatcher__loadProducts(products)
        self.matcher._ProductListingMatcher__matchListings([listing])
        
        for product_set in (filter(lambda x: len(x) != 0, self.matcher._ProductListingMatcher__product_dict.values())):
            product, = product_set
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
    
    def testAccessoryListingNotMatched(self):
        """ We shouldn't match if a listing appears to match multiple products. """
        products = ["""{"product_name":"Nikon_D3000","manufacturer":"Nikon","model":"D3000","announced-date":"2009-07-29T20:00:00.000-04:00"}""",
                   """{"product_name":"Nikon_D5000","manufacturer":"Nikon","model":"D5000","announced-date":"2009-04-13T20:00:00.000-04:00"}"""]
        listing = """{"title":"Nikon EN-EL9a 1080mAh Ultra High Capacity Li-ion Battery Pack for Nikon D40, D40x, D60, D3000, & D5000 Digital SLR Cameras","manufacturer":"Nikon","currency":"CAD","price":"29.75"}"""
        self.__testListingMatched(products, listing, should_match=False)
        
        
        
