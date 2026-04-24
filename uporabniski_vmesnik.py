import os
from datetime import datetime

# --- Uvoz modulov ---
from zbiranje_podatkov.pobiralec import poberi_vse_strani, shrani_json
from napovedni_model import (
    preberi_podatke,
    pripravi_matrike,
    treniraj_model,
    najdi_podcenjene,
    izris_pomembnosti
)
from analiza import (
    slika_zaloge_znamk,
    slika_prodanih_znamk,
    slika_goriv,
    slika_analiza_modela,
    slika_ugodnost_znamk
)

# --- Poti ---
MAPA_ARHIV = os.path.join("data", "arhiv")


# ---------------------------------------------------------
# 1) Izbira podatkov
# ---------------------------------------------------------

def ime_danes():
    return f"span_avti_{datetime.now().strftime('%d-%m-%Y')}.json"


def preveri_danes():
    ime = ime_danes()
    pot = os.path.join(MAPA_ARHIV, ime)
    return pot if os.path.exists(pot) else None


def pridobi_danes():
    pot = preveri_danes()
    if pot:
        print(f"Današnji podatki že obstajajo: {pot}")
        return pot

    print("Pridobivam današnje podatke (5 min)...")
    avti = poberi_vse_strani()

    ime = ime_danes()
    pot = os.path.join(MAPA_ARHIV, ime)
    shrani_json(avti, pot)

    print(f"Današnji podatki shranjeni v: {pot}")
    return pot


def izberi_arhiv():
    datoteke = sorted(f for f in os.listdir(MAPA_ARHIV) if f.endswith(".json"))

    if not datoteke:
        print("Ni arhivskih datotek.")
        return None

    print("\nArhivske datoteke:")
    for i, f in enumerate(datoteke, 1):
        print(f"{i}) {f}")

    izbira = input("\nIzberi številko datoteke: ")

    try:
        idx = int(izbira) - 1
        return os.path.join(MAPA_ARHIV, datoteke[idx])
    except:
        print("Neveljavna izbira.")
        return None


# ---------------------------------------------------------
# 2) MODEL – Najugodnejši avto (z znamko, ceno, številom rezultatov)
# ---------------------------------------------------------

def najugodnejši_avto(pot):
    avti = preberi_podatke(pot)

    # -----------------------------
    # 1) Filtri
    # -----------------------------
    print("\nFiltri (pusti prazno za brez filtra):")

    filter_znamka = input("Znamka (npr. audi): ").strip().lower()
    filter_min_cena = input("Minimalna cena: ").strip()
    filter_max_cena = input("Maksimalna cena: ").strip()

    # Pretvorba cen
    min_cena = int(filter_min_cena) if filter_min_cena else None
    max_cena = int(filter_max_cena) if filter_max_cena else None

    # Uporaba filtrov
    filtrirani = []
    for v in avti:
        if filter_znamka and v["znamka"].lower() != filter_znamka:
            continue
        if min_cena is not None and v["cena"] < min_cena:
            continue
        if max_cena is not None and v["cena"] > max_cena:
            continue
        filtrirani.append(v)

    if not filtrirani:
        print("\nNi vozil, ki ustrezajo filtrom.")
        return

    # -----------------------------
    # 2) Koliko rezultatov želi uporabnik
    # -----------------------------
    try:
        n = int(input("\nKoliko najugodnejših avtov želiš prikazati? "))
    except:
        n = 3

    # -----------------------------
    # 3) Model
    # -----------------------------
    X, y = pripravi_matrike(filtrirani)
    model = treniraj_model(X, y)

    top = najdi_podcenjene(filtrirani, model, n=n)

    # -----------------------------
    # 4) Izpis rezultatov
    # -----------------------------
    print("\nNajbolj podcenjeni avti:\n")
    for v in top:
        print(f"{v['naziv']}")
        print(f"  Cena: {v['cena']}")
        print(f"  Napoved: {v['napoved']:.0f}")
        print(f"  Razlika: {v['razlika']:.0f}")
        print(f"  Link: {v.get('link', '—')}\n")

    #print("Odpiram graf pomembnosti...")
    #izris_pomembnosti(model, ["km", "kw", "starost", "km_leto"])


# ---------------------------------------------------------
# 3) MODEL – Napoved cene za ročni vnos
# ---------------------------------------------------------

def napovej_ceno(pot):
    avti = preberi_podatke(pot)
    X, y = pripravi_matrike(avti)
    model = treniraj_model(X, y)

    print("\nVnesi podatke o vozilu:")
    letnik = int(input("Letnik: "))
    km = int(input("Prevoženi km: "))
    kw = int(input("Moč motorja (kW): "))

    starost = 2026 - letnik
    km_leto = km / starost if starost > 0 else km

    X_new = [[km, kw, starost, km_leto]]
    napoved = model.predict(X_new)[0]

    print(f"\nNapovedana cena: {napoved:.0f} €")


# ---------------------------------------------------------
# 4) Analiza trga
# ---------------------------------------------------------

def analiza_trga(pot):
    print("\nOdpiram analitične grafe...")

    slika_zaloge_znamk(pot)
    slika_prodanih_znamk(pot)
    slika_goriv(pot)
    slika_ugodnost_znamk(pot)

    znamka = input("\nVnesi znamko za analizo modelov (npr. volkswagen): ").strip()
    if znamka:
        slika_analiza_modela(pot, znamka)


# ---------------------------------------------------------
# 5) Glavni meni
# ---------------------------------------------------------

def main():
    os.makedirs(MAPA_ARHIV, exist_ok=True)

    print("\n=========================================")
    print("  Izberi podatke za delo")
    print("=========================================")
    print("1) Današnji podatki")
    print("2) Arhivski podatki")

    izbira = input("\nIzberi možnost: ").strip()

    if izbira == "1":
        pot = pridobi_danes()
    elif izbira == "2":
        pot = izberi_arhiv()
        if not pot:
            return
    else:
        print("Neveljavna izbira.")
        return

    # --- Glavni meni po izbiri podatkov ---
    while True:
        print("\n=========================================")
        print("  Kaj želiš narediti?")
        print("=========================================")
        print("1) Najti najugodnejši avto")
        print("2) Napovedati ceno za ročni vnos")
        print("3) Analiza trga")
        print("4) Izhod")

        izbira = input("\nIzberi možnost: ").strip()

        if izbira == "1":
            najugodnejši_avto(pot)

        elif izbira == "2":
            napovej_ceno(pot)

        elif izbira == "3":
            analiza_trga(pot)

        elif izbira == "4":
            print("Izhod.")
            break

        else:
            print("Neveljavna izbira.")


if __name__ == "__main__":
    main()
