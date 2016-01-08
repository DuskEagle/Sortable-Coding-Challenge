from Normalizer import *

class Product:
    
    def __init__(self, json):
        """ json is a Pyhton dictionary made from calling json.loads()
        on a JSON string """
        self.json = json
        self.product_name = genericNormalizer(json["product_name"])
        self.manufacturer = manufacturerNormalizer(json["manufacturer"])
        self.family = genericNormalizer(json.get("family", ""))
        self.model = genericNormalizer(json["model"])
        self.announced_date = json["announced-date"]
    