def manufacturerNormalizer(manufacturer):
    """ Given a string for the name of a manufacturer, convert this string into
    a "normalized" form so that slightly different names for the same
    manufacturer are considered as equal. """
    
    """ Strip all but the first word from the manufacturer string and convert
    to lower case. """
    manufacturer = manufacturer.split(' ')[0].split('-')[0].lower()
    
    """ Special case for Hewlett-Packard"""
    if manufacturer == "hewlett": 
        manufacturer = "hp"
    
    return manufacturer

def genericNormalizer(string):
    """ For a generic field, convert to a normalized form to make string
    comparison simpler. Currently, just converts the string to all lower case. """
    
    return string.lower()