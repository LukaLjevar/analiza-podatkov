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
id_produktov = []
ime_produktov = []
ocene = []
opisi = []
razpoložljivosti = []
partneji = []
cene = []

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

bloki = združena_juha.find_all("div", {"class": "pbcr"})

for blok in bloki:

    id_produkta = blok.get("id", "N/A")
    id_produktov(id_produkta)

    ime_produkta = blok.find("span", {"class": "pbcr__title"})
    ime_produktov.append(ime_produkta.text.strip() if ime_produkta else "N/A" )

    ocena = blok.find("span", {"data-testid": "rating-count"})
    ocene.append(ocenaa.text.strip() if ocena else "N/A")

    opis = blok.find("p")
    opisi.append(opis.text.strip() if opis else "N/A")

    razpoložljivost = blok.find("p", {"data-testid": "availability-tooltip-text"})
    razpoložljivosti.append(razpoložljivost.text.strip() if razpoložljivost else "N/A")

    partner = blok.find("b")
    partnerji.append(partner.text.strip() if partner else "N/A")

    cena = blok.find("span", {"data-sel": "product-box-price"})
    cene.append(cena.text.strip() if cena else "N/A")



df = pd.DataFrame({
    "ID_Produkta": id_produktov,
    "Ime_Produkta": ime_produktov,
    "Ocena": ocene,
    "Opis": opisi,
    "Razpoložljivost": razpoložljivosti,
    "Partner": partneji,
    "Cena": cene
})