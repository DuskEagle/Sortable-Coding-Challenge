import re

from Normalizer import *

class Product:
    
    def __init__(self, obj):
        """ obj is a Python dictionary made from calling json.loads()
        on a JSON string """
        self.obj = obj
        
        """ We don't match on product_name, but we need it for printing, so we
        don't normalize this field. """
        self.product_name = obj["product_name"]
        
        self.manufacturer = manufacturerNormalizer(obj["manufacturer"])
        
        """ If a product does not have a family, self.family == "" """
        self.family = genericNormalizer(obj.get("family", ""))
        
        self.model = genericNormalizer(obj["model"])
        self.model_regex = self.__makeModelRegex()
        self.announced_date = obj["announced-date"]
    
    def __makeModelRegex(self):
        regex_builder = []
        for i in range(len(self.model)):
            letter = self.model[i]
            
            """ We want to ignore these characters in our search, as each individual
            listing varies too much on whether they are included. """
            if letter == ' ' or letter == '-':
                letter = "[ -]?"
            elif not letter.isalnum():
                """ Escape characters that will cause problems in the regex. """
                letter = "\\" + letter
            
            if i < len(self.model)-1:
                regex_builder.append(letter + "[ -]?")
            else:
                regex_builder.append(letter)
        return re.compile("\\b" + "".join(regex_builder)  + "\\b")
    
    
    
    def __eq__(self, other):
        """ We ignore product_name and announced_date since we don't match listings
        off of those fields. """
        if isinstance(other, Product):
            return self.manufacturer == other.manufacturer \
                and self.model == other.model \
                and self.family == other.family
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        return result if result == NotImplemented else not result
    
    def __hash__(self):
        """ Must define explicitly because we also defined __eq__ explicitly. """
        return hash((self.manufacturer, self.model, self.family))