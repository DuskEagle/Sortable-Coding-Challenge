from Normalizer import *

class Listing:
    def __init__(self, obj):
        """ obj is a Python dictionary made from calling json.loads()
        on a JSON string """
        self.obj = obj
        self.title = self.__cropTitle(genericNormalizer(obj["title"]))
        self.manufacturer = manufacturerNormalizer(obj["manufacturer"])
        self.currency = obj["currency"]
        self.price = obj["price"]
        
    def __cropTitle(self, title_string):
        """ Crop the (already normalized) title string so we get less false positive
        matchings.
        
        To do this, we will remove everything from the title string after and
        including the word "for", to eliminate results such as "Camera bag for
        <model name>". We'll do this for translations of "for" in a few different
        languages, which can be expanded as needed. """
        
        """ English, French, German, Spanish """
        translations_of_for = ["for", "pour", "für", "para"]
        
        for string in translations_of_for:
            """ Alternatively, "for for in fors" ;) """
            title_string = title_string.split(" " + string + " ")[0]
        return title_string