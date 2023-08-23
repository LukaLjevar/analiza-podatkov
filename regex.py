import re
from pathlib import Path

def poisci_bloke():
    bloki = []
    #with open("stran1.html") as dat:
    with Path(f'C:/Users/luka/Desktop/Projektna UVP/stran1.html').open(mode='r', encoding='utf-8') as dat:
        besedilo = dat.read()

        vzorec_bloka = re.compile(
            '<b>Mimovrste</b>' r'.*?' 'Partner:',
            flags=re.DOTALL,
        )

        for najdba in vzorec_bloka.finditer(besedilo):
            bloki.append(besedilo[najdba.start() : najdba.end()])

    return bloki
bloki = poisci_bloke()
#########################################################################################################################################

def izlusci_podatke(blok):
    zmrzovalnik = {}

    # izluscimo tip zmrzovalnika
    vzorec1 = re.compile(
        r'hidden-title">' r'(?P<tip>.*?)' '</span></a>', flags=re.DOTALL,

    )
    najdba = vzorec1.search(str(blok))
    zmrzovalnik["tip"] = najdba["tip"]

    # izluscimo ceno
    vzorec_cena = re.compile(
        r'price"><span>.' r'(?P<cena>.*?)' '<!----></span>', flags=re.DOTALL,
    )
    najdba = vzorec_cena.search(str(blok))
    zmrzovalnik["cena"] = najdba["cena"]


    return zmrzovalnik

z = izlusci_podatke(blok=bloki)
print(z)


