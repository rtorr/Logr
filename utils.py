import re

def slugify(text):
    """
    Generates an ASCII-only slug.
    """
    return re.sub('-$', '', re.sub('[^A-Za-z0-9\-]+', '-', text))
