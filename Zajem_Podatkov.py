import requests
from pathlib import Path
def zajem_podatkov(n):
    for i in range(n):
        stran = requests.get(f"https://www.mimovrste.com/zamrzovalniki?pagination={i + 1}")
        print(f"loop{i+1}")
        print(stran.text)

        with Path(f'./stran{i+1}.html').open(mode='w', encoding='utf-8') as dat:
            dat.write(stran.text)
