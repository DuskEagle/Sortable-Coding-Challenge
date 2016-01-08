from Normalizer import *

class Listing:
    def __init__(self, json):
        """ json is a Pyhton dictionary made from calling json.loads()
        on a JSON string """
        self.json = json
        self.title = genericNormalizer(json["title"])
        self.manufacturer = manufacturerNormalizer(json["manufacturer"])
        self.currency = json["currency"]
        self.price = json["price"]