from bs4 imort BeautifulSoup, Tag, NavigableString
import pandas as pd

def ali_ima_list_besedilo(element):
        if isinstance(element, NavigableString):
            return True
        if isinstance(element, Tag):
            return any(ali_ima_list_besedilo(otrok) for otrok in element.children)
        return False