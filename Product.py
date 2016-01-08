class Product:
    
    def __init__(self, product_json):
        self.product_name = product_json["product_name"]
        self.manufacturer = product_json["manufacturer"]
        self.family = product_json.get("family", None)
        self.model = product_json["model"]
        self.announced_date = product_json["announced-date"]
    