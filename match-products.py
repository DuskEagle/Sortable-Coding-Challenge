from collections import defaultdict, OrderedDict
import json

from Listing import Listing
from Product import Product
from Result import Result

products_filename = "data/products.txt"
listings_filename = "data/listings.txt"
results_filename = "results.txt"

products_file = open(products_filename)
products_string = products_file.read().splitlines()
products_file.close()

""" We assume manufacturers and product families will correspond to multiple
products, but that a pair (manufacturer, model) will correspond to exactly
one product. This is true for our current data, and we assume whatever code
generates our product list ensures this remains the case. """
product_manufacturer_dict = defaultdict(list)
product_family_dict = defaultdict(list)
product_manufacturer_model_dict = {}

for product_string in products_string:
    product = Product(json.loads(product_string))
    #FIXME We don't use this dict as anything but a list
    product_manufacturer_dict[product.manufacturer].append(product)
    #FIXME We don't use this dict
    product_family_dict[product.family].append(product)
    product_manufacturer_model_dict[(product.manufacturer, product.model)] = product

listings_file = open(listings_filename)
listings_string = listings_file.read().splitlines()
listings_file.close()

product_listing_dict = defaultdict(list)

manufacturers = product_manufacturer_dict.keys()
manufacturer_model_pairs = product_manufacturer_model_dict.keys()
families = product_family_dict.keys()

for listing_string in listings_string:
    """ We load into an OrderedDict to preserve the ordering of the fields when
    we print back to JSON. This is not strictly necessary, but it makes it nicer
    for people to read. """
    listing = Listing(OrderedDict(json.loads(listing_string)))
    
    product_matched = None
    for manufacturer, model in manufacturer_model_pairs:
        if manufacturer == listing.manufacturer and " " + model + " " in listing.title:
            if product_matched != None:
                product_matched = None
                break
            else:
                product_matched = product_manufacturer_model_dict[(manufacturer, model)]
    
    if product_matched != None:
        product_listing_dict[product_matched].append(listing)

results_file = open(results_filename, "w")
for product in product_listing_dict.keys():
    result = Result(product, product_listing_dict[product])
    results_file.write(result.toJson())
results_file.close()    
  


