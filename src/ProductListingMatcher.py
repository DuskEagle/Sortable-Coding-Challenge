from collections import defaultdict, OrderedDict
import json
import re

from Listing import Listing
from MultipleProductsMatchedException import MultipleProductsMatchedException
from Product import Product
from Result import Result

class ProductListingMatcher:

    def __init__(self, products_filename, listings_filename, results_filename):
        self.__products_filename = products_filename
        self.__listings_filename = listings_filename
        self.__results_filename = results_filename

        self.__product_dict = defaultdict(set)
        self.__product_listing_dict = defaultdict(list)
    
    def match(self):
        products_strings = self.__loadFromFile(self.__products_filename)
        self.__loadProducts(products_strings)
        listings_strings = self.__loadFromFile(self.__listings_filename)
        self.__matchListings(listings_strings)
        self.__writeResults()
    
    def __loadFromFile(self, filename):
        fp = open(filename)
        strings = fp.read().splitlines()
        fp.close()
        return strings
        
    
    def __loadProducts(self, products_strings):
        
        for product_string in products_strings:
            product = Product(json.loads(product_string))

            if product not in self.__product_dict[(product.manufacturer, product.model_regex)]: # Ignore duplicates
                self.__product_dict[(product.manufacturer, product.model_regex)].add(product)

        self.__manufacturer_model_pairs = self.__product_dict.keys()

    def __matchListings(self, listings_strings):
        
        for listing_string in listings_strings:
            
            """ We load into an OrderedDict to preserve the ordering of the fields when
            we print back to JSON. This is not strictly necessary, but it makes it nicer
            for people to read. """
            listing = Listing(json.loads(listing_string, object_pairs_hook=OrderedDict))
            
            product_matched = None
            
            try:
                for manufacturer, model_regex in self.__manufacturer_model_pairs:
                    if manufacturer == listing.manufacturer and model_regex.search(listing.title):
                        if product_matched != None:
                            raise MultipleProductsMatchedException
                        else:
                            product_set = self.__product_dict[(manufacturer, model_regex)]
                            """ If there's only one product matching this (manufacturer, model_regex)
                            pair, then match the listing to it. Otherwise, we will need to look
                            at the product families to see which one matches. """
                            if len(product_set) == 1:
                                """ Weird syntax for assigning the one element in product_set to
                                product_matched. """
                                product_matched, = product_set
                            else:
                                for product in product_set:
                                    if product.family != "" and product.family in listing.title:
                                        if product_matched != None:
                                            raise MultipleProductsMatchedException
                                        product_matched = product
            except MultipleProductsMatchedException:
                product_matched = None
                                
            if product_matched != None:
                self.__product_listing_dict[product_matched].append(listing)

    def __writeResults(self): 
        results_file = open(self.__results_filename, "w")
        for product_set in self.__product_dict.values():
            for product in product_set:
                result = Result(product, self.__product_listing_dict[product])
                results_file.write(result.toJson())
                results_file.write("\n")
        results_file.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        products_filename = "data/products.txt"
        listings_filename = "data/listings.txt"
        results_filename = "data/results.txt"
    elif len(sys.argv) == 4:
        products_filename, listings_filename, results_filename = sys.argv[1:4]
    else:
        print("Usage: python " + sys.argv[0] + " [products_file, listings_file, results_file]")
        sys.exit()
    
    matcher = ProductListingMatcher(products_filename, listings_filename, results_filename)
    matcher.match()
    



