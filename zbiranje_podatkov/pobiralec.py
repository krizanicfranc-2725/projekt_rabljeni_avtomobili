import re
import time
import json
import requests
from zbiranje_podatkov.iskalec import najdi_avto


headers = {"User-Agent": "Chrome/145.0.7632.160"}

def prenesi_stran(n):
    # vrne html tekst n-te strani trgovine span 
    url = f"https://trgovina.span.si/sl/Rabljena-vozila/p{n}.html"
    r = requests.get(url, headers=headers, timeout=10)
    return r.text if r.status_code == 200 else ""

def split_na_avte(html):
    # razdeli html tekst na bloke, ki ustrezajo posameznim avtomobilom
    return re.split(r'<div class="item-box[^"]*">', html)[1:]

def format_cas(sekunde):
    minute = int(sekunde // 60)
    sek = int(sekunde % 60)
    return f"{minute} min {sek} s"

def poberi_vse_strani():
    #poberi podatke o vseh avtomobilih z vseh strani trgovine span

    # Koliko strani sploh obstaja
    html_prva = prenesi_stran(1)
    m = re.search(r"bcmsPagingLastPage[^>]*>.*?p(\d+)\.html", html_prva)
    max_stran = int(m.group(1)) if m else 1
    print(f"Najdeno število strani: {max_stran}")

    vsi_avti = []
    zacetek = time.time()

    for stran in range(1, max_stran + 1):
        start_page = time.time()
        html = prenesi_stran(stran)
        bloki = split_na_avte(html)

        print(f"Stran {stran}/{max_stran}: v {time.time() - start_page:.3f} s")

        for blok in bloki:
            avto = najdi_avto(blok)
            if avto and avto.id is not None:

                # izloči najemne avte
                if avto.cena is not None and avto.cena < 1000:
                    continue
                if avto.znamka and avto.znamka.lower().startswith("citro"):
                    avto.znamka = "citroen"
                if avto.znamka and avto.znamka.lower().startswith("mercedes"):
                    avto.znamka = "mercedes"
                if avto.znamka and avto.znamka.startswith("land"):
                    avto.znamka = "land rover"

                vsi_avti.append(avto)


    skupni = time.time() - zacetek
    print(f"\nSkupni čas pobiranja: {format_cas(skupni)}")
    print(f"Skupno najdenih avtov: {len(vsi_avti)}")

    return vsi_avti

def shrani_json(avti, pot):
    with open(pot, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in avti], f, ensure_ascii=False, indent=4)

    print(f"Podatki shranjeni v {pot}")
