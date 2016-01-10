from collections import OrderedDict

import json

from Product import Product
from Listing import Listing

class Result:
    def __init__(self, product, listings):
        self.product = product
        self.listings = listings
    
    def toJson(self):
        """ We use an OrderedDict here to ensure product_name comes first in the
        JSON output, which is nicer to read for people."""
        return json.dumps(OrderedDict([("product_name", self.product.product_name),
                                       ("listings", [listing.obj for listing in self.listings])]))

