from Normalizer import *

class Listing:
    def __init__(self, obj):
        """ obj is a Pyhton dictionary made from calling json.loads()
        on a JSON string """
        self.obj = obj
        self.title = genericNormalizer(obj["title"])
        self.manufacturer = manufacturerNormalizer(obj["manufacturer"])
        self.currency = obj["currency"]
        self.price = obj["price"]