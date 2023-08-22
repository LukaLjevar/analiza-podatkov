import requests
from pathlib import Path

for i in range(6):
    stran = requests.get(f"https://www.mimovrste.com/zamrzovalniki?pagination={i + 1}")
    print(f"loop{i+1}")
    print(stran.text)
    
    with Path(f'C:/Users/luka/Desktop/Projektna UVP/stran{i+1}.html').open(mode='w', encoding='utf-8') as dat:
        dat.write(stran.text)
