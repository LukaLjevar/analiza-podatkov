from bs4 imort BeautifulSoup, Tag, NavigableString
import pandas as pd

def obreži_html_drevo(element):
    for otrok in list(element.children):
        if isinstance(otrok, Tag):
            if not any(x.strip for x in otrok.stripped_strings):
                otrok.extract()

            else:
                prune_tree(otrok)


def odstrani_vizualne_element(juha):
    for element in juha(['script', 'style', 'link', 'meta', 'noscript', 'img']):
        element.decompose()

def izlušči_relevantne_dive(juha):
    return juha.find('div', {'class': 'category-products'})
