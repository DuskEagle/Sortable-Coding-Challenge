from collections import defaultdict
import json

from Product import Product
from Listing import Listing

products_file = open("data/products.txt")
listings_file = open("data/listings.txt")

products_string = products_file.read().splitlines()

""" We assume manufacturers and product families will correspond to multiple
products, but that a pair (manufacturer, model) will correspond to exactly
one product. This is true for our current data, and we assume whatever code
generates our product list ensures this remains the case. """
product_manufacturer_dict = defaultdict(list)
product_family_dict = defaultdict(list)
product_manufacturer_model_dict = {}

for product in products_string:
    product = Product(json.loads(product))
    product_manufacturer_dict[product.manufacturer].append(product)
    product_family_dict[product.family].append(product)
    product_manufacturer_model_dict[(product.manufacturer, product.model)] = product
    
listings_string = listings_file.read().splitlines()

product_listing_dict = defaultdict(list)

manufacturers = product_manufacturer_dict.keys()
manufacturer_model_pairs = product_manufacturer_model_dict.keys()
families = product_family_dict.keys()

for listing in listings_string:
    listing = Listing(json.loads(listing))
    
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

for product in product_listing_dict.keys():
    print (product.product_name, product.manufacturer, product.model, product.family)
    
    for listing in product_listing_dict[product]:
        print(listing.manufacturer + ": " + listing.title)
    print("\n-----\n")


