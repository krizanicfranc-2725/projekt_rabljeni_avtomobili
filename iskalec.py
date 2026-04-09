import re
from avto import Avto

def najdi_avto(html):

    # ID  <h3><a href="/sl/Rabljena-vozila/Mercedes-Benz-CLA Shooting Brake-Vozilo201627/
    m = re.search(r"Vozilo(\d+)", html)
    id = int(m.group(1)) if m else None

    # Naziv  <h3><a href="/sl/Rabljena-vozila/Mercedes-Benz-CLA Shooting Brake-Vozilo201627/
    m = re.search(r"<h3>.*?<a[^>]*>([^<]*)</a>", html)
    naziv = m.group(1).strip() if m else None

    # Znamka  <h3><a href="/sl/Rabljena-vozila/Mercedes-Benz-CLA Shooting Brake-Vozilo201627/
    m = re.match(r"([A-Za-zČŠŽčšž\-]+)", naziv) if naziv else None
    znamka = m.group(1) if m else None

    # Gorivo  <h4><a href="/sl/Rabljena-vozila/Mercedes-Benz-CLA Shooting Brake-Vozilo201627/">dizelski
    m = re.search(r"<h4>.*?<a[^>]*>([^,]*)", html)
    gorivo = m.group(1).strip() if m else None

    # Prostornina  Vozilo201627/">dizelski, 1950 ccm, 110kW / 150 KM
    m = re.search(r"(\d+)\s*ccm", html)
    prostornina = int(m.group(1)) if m else None

    # Moč (kW)  Vozilo201627/">dizelski, 1950 ccm, 110kW / 150 KM
    m = re.search(r"(\d+)\s*kW", html)
    kw = int(m.group(1)) if m else None

    # Moč (KM)  Vozilo201627/">dizelski, 1950 ccm, 110kW / 150 KM
    m = re.search(r"/\s*(\d+)\s*KM", html)
    km_motor = int(m.group(1)) if m else None

    # Letnik  <b>letnik:</b> 2025
    m = re.search(r"<b>letnik:</b>\s*(\d+)", html)
    letnik = int(m.group(1)) if m else None

    # Kilometri  <b>Prevoženo:</b> 17292
    m = re.search(r"<b>Prevoženo:</b>\s*([\d\.]+)", html)
    km = int(m.group(1).replace(".", "")) if m else None

    # Menjalnik  <b>Menjalnik:</b> avtomatski
    m = re.search(r"<b>Menjalnik:</b>\s*([^<]*)", html)
    menjalnik = m.group(1).strip() if m else None

    # Cena (z ali brez financiranja)
    #   <strong class="is-financing-price">€ 35.953</strong>
    #   <strong>€ 29.999</strong>
    m = re.search(r'class="is-financing-price">&euro;\s*([\d\.]+)', html)
    if m:
        cena = int(m.group(1).replace(".", ""))
    else:
        m = re.search(r'<strong>&euro;\s*([\d\.]+)</strong>', html)
        cena = int(m.group(1).replace(".", "")) if m else None

    # Cena s financiranjem  <span>Cena s financiranjem:</span> <strong>€ 29.469</strong>
    m = re.search(r'<span>Cena s financiranjem:</span>\s*<strong>&euro;\s*([\d\.]+)</strong>', html)
    cena_fin = int(m.group(1).replace(".", "")) if m else None

    # Prodano  <div class="item-box sold-out">  ali  <h3>Prodano</h3>
    prodano = "sold-out" in html or bool(re.search(r"<h3>\s*Prodano\s*</h3>", html))

    return Avto(
        id, naziv, znamka, gorivo, letnik, km, menjalnik,
        cena, cena_fin, prodano, prostornina, kw, km_motor
    )
