from bs4 imort BeautifulSoup, Tag, NavigableString
import pandas as pd

def obreži_html_drevo(element):
    for otrok in list(element.children):
        if isinstance(otrok, Tag):
            if not any(x.strip for x in otrok.stripped_strings):
                otrok.extract()

            else:
                prune_tree(otrok)


def odstrani_vizualne_elemente(juha):
    for element in juha(['script', 'style', 'link', 'meta', 'noscript', 'img']):
        element.decompose()

def izlušči_relevantne_dive(juha):
    return juha.find('div', {'class': 'category-products'})

podatki = []
id_produkta = []
ime_produkta = []
ocena = []
opis = []
razpoložljivost = []
partner = []
cena = []

združena_juha = BeautifulSoup('', 'html.parser')

for i in range(1, 7):

    with open(f'stran{i}.html', 'r', encoding = 'utf-8') as f:
        html_vsebina = f.read()

    juha = BeautifulSoup(html_vsebina, 'html.parser')

    obreži_html_drevo(juha)
    odstrani_vizualne_elemente(juha)

    relevanten_div = izlušči_relevantne_dive(juha)

    if relevanten_div:
        združena_juha.body.append(relevanten_div)

    else:
        print(f"'category_products' div na strani{i} ni bil najden")