from collections import defaultdict
import json

from Product import Product
from Listing import Listing

products_file = open("data/products.txt")
listings_file = open("data/listings.txt")

products_string = products_file.read().splitlines()

product_manufacturer_dict = defaultdict(list)
product_model_dict = defaultdict(list)
product_family_dict = defaultdict(list)

for product in products_string:
    product = Product(json.loads(product))
    product_manufacturer_dict[product.manufacturer].append(product)
    product_model_dict[product.model].append(product)
    product_family_dict[product.family].append(product)
    
listings_string = listings_file.read().splitlines()

product_listing_dict = defaultdict(list)

for listing in listings_string:
    listing = Listing(json.loads(listing))
    for model in product_model_dict.keys():
        if model in listing.title:
            products = product_model_dict[model]
            if len(products) > 1:
                #raise RuntimeError("More than one model with same name: " + model)
                continue
            product_listing_dict[products[0]].append(listing)

for product, listings in product_listing_dict.items():
    print (product.product_name, product.manufacturer, product.model)
    print("")
    for listing in listings:
        print (listing.title, listing.price)
    print ("\n----")



