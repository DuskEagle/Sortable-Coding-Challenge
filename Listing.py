class Listing:
    def __init__(self, listing_json):
        self.title = listing_json["title"]
        self.manufacturer = listing_json["manufacturer"]
        self.currency = listing_json["currency"]
        self.price = listing_json["price"]