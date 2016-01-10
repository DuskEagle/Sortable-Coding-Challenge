from collections import defaultdict, OrderedDict
import json
import re

from Listing import Listing
from MultipleProductsMatchedException import MultipleProductsMatchedException
from Product import Product
from Result import Result

products_filename = "data/products.txt"
listings_filename = "data/listings.txt"
results_filename = "results.txt"

products_file = open(products_filename)
products_string = products_file.read().splitlines()
products_file.close()

manufacturers = set()
product_dict = defaultdict(set)

for product_string in products_string:
    product = Product(json.loads(product_string))
    manufacturers.add(product.manufacturer)

    if product not in product_dict[(product.manufacturer, product.model_regex)]: # Ignore duplicates
        product_dict[(product.manufacturer, product.model_regex)].add(product)


listings_file = open(listings_filename)
listings_string = listings_file.read().splitlines()
listings_file.close()

product_listing_dict = defaultdict(list)

manufacturer_model_pairs = product_dict.keys()

for listing_string in listings_string:
    """ We load into an OrderedDict to preserve the ordering of the fields when
    we print back to JSON. This is not strictly necessary, but it makes it nicer
    for people to read. """
    
    listing = Listing(json.loads(listing_string, object_pairs_hook=OrderedDict))
    
    product_matched = None
    
    try:
        for manufacturer, model_regex in manufacturer_model_pairs:
            if manufacturer == listing.manufacturer and model_regex.search(listing.title):
                if product_matched != None:
                    raise MultipleProductsMatchedException
                else:
                    product_set = product_dict[(manufacturer, model_regex)]
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
        product_listing_dict[product_matched].append(listing)

results_file = open(results_filename, "w")
for product_set in product_dict.values():
    for product in product_set:
        result = Result(product, product_listing_dict[product])
        results_file.write(result.toJson())
        results_file.write("\n")
results_file.close()

