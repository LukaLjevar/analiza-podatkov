from bs4 import BeautifulSoup, Tag
import pandas as pd

pd.set_option( 'display.max_columns', None)

# Funkcija, ki odstrani elemente, ki ne vsebujejo besedila v listu.
def obreži_html_drevo(element):
    for otrok in list(element.children):
        if isinstance(otrok, Tag):
            if not any(x.strip for x in otrok.stripped_strings):
                otrok.extract()

            else:
                obreži_html_drevo(otrok)


# Funkcija, ki iz HTML-ja odstrani vizualne elemente.
def odstrani_vizualne_elemente(juha):
    for element in juha(['script', 'style', 'link', 'meta', 'noscript', 'img']):
        element.decompose()

# Funkcija, ki iz HTML-ja izlušči relevantne dele.
def izlušči_relevantne_dive(juha):
    return juha.find('div', {'class': 'category-products'})

podatki = []
id_produktov = []
ime_produktov = []
ocene = []
opisi = []
razpoložljivosti = []
partnerji = []
cene = []

združena_juha = BeautifulSoup('', 'html.parser')

# Funkcija, ki izlušči relevantne dele vsakega HTML-ja.
def izlušči_grobo(m,n):
    for i in range(m, n):

        #with Path(f'C:/Users/luka/Desktop/Projektna UVP/analiza-podatkov/stran{i}.html').open(mode='r', encoding='utf-8') as f:

        with open(f'stran{i}.html', 'r', encoding = 'utf-8') as f:
            html_vsebina = f.read()

        juha = BeautifulSoup(html_vsebina, 'html.parser')

        obreži_html_drevo(juha)
        odstrani_vizualne_elemente(juha)

        relevanten_div = izlušči_relevantne_dive(juha)

        if relevanten_div:
            #združena_juha.body.append(relevanten_div)
            združena_juha.append(relevanten_div)
        else:
            print(f"'category_products' div na strani{i} ni bil najden")


# Funkcija, ki izluščene podatke zapiše v Pandas DataFrame in csv.
def izlušči_in_zapiši():
    bloki = združena_juha.find_all("div", {"class": "pbcr"})
    for blok in bloki:

        id_produkta = blok.get("id", "N/A")
        id_produktov.append(id_produkta)

        ime_produkta = blok.find("span", {"class": "pbcr__title"})
        ime_produktov.append(ime_produkta.text.strip() if ime_produkta else "N/A" )

        ocena = blok.find("span", {"data-testid": "rating-count"})
        ocene.append(int(ocena.text.strip().strip("x").strip()) if ocena else "N/A")


        opis = blok.find("p")
        opisi.append(opis.text.strip() if opis else "N/A")

        razpoložljivost = blok.find("p", {"data-testid": "availability-tooltip-text"})
        razpoložljivosti.append(razpoložljivost.text.strip("na voljo predvidoma:\n        ") if razpoložljivost else "N/A")

        partner = blok.find("b")
        partnerji.append(partner.text.strip() if partner else "N/A")

        cena = blok.find("span", {"data-sel": "product-box-price"})
        cene.append(float(cena.text.strip().strip("€").strip().replace(".", "").replace(",", ".")) if cena else "N/A")

    df = pd.DataFrame({
        "ID_Produkta": id_produktov,
        "Ime_Produkta": ime_produktov,
        "Število_Ocen": ocene,
        "Opis": opisi,
        "Razpoložljivost": razpoložljivosti,
        "Partner": partnerji,
        "Cena_v_Evrih": cene
    })

    #df.to_csv("podatki.csv", sep=";")

    # Odstranjevanje &nbps
    df.replace("\xa0", ' ', regex=True, inplace=True)
    # Odstrani stolpec index
    df.drop(df.columns[[0]], axis=1, inplace=True)
    # Prevtorba stolpca v tip integer
    df['Število_Ocen'] = df['Število_Ocen'].replace('N/A', '0')
    df['Število_Ocen'] = df['Število_Ocen'].astype(int)
    # Shrani csv brez &nbps
    df.to_csv("podatki.csv", sep=";")
