import os
from datetime import datetime

# Uvoz modulov
from zbiranje_podatkov.pobiralec import poberi_vse_strani, shrani_json
from napovedni_model import (
    preberi_podatke,
    pripravi_matrike,
    treniraj_model,
    najdi_podcenjene
)
from analiza_UV import analiza_UV

# Pot do podatkov
MAPA_ARHIV = os.path.join("data", "arhiv")

# 1) Izbira podatkov

def ime_danes():
    "Vrne ime datoteke za današnje podatke."
    return f"span_avti_{datetime.now().strftime('%d-%m-%Y')}.json"


def preveri_danes():
    "Preveri, ali današnji podatki že obstajajo in vrne pot do njih."
    ime = ime_danes()
    pot = os.path.join(MAPA_ARHIV, ime)
    return pot if os.path.exists(pot) else None


def pridobi_danes():
    "Pridobi današnje podatke, če že obstajajo, jih prebere, sicer jih pobere in shrani."
    pot = preveri_danes()
    if pot:
        print(f"Današnji podatki že obstajajo: {pot}")
        return pot

    print("Pridobivam današnje podatke (približno 5 min)...")
    avti = poberi_vse_strani()

    ime = ime_danes()
    pot = os.path.join(MAPA_ARHIV, ime)
    shrani_json(avti, pot)

    print(f"Današnji podatki shranjeni v: {pot}")
    return pot


def izberi_arhiv():
    "Prikaže seznam arhivskih datotek in omogoči izbiro."
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


# Najugodnejši avto (z znamko, ceno, številom rezultatov)

def najugodnejši_avto(pot):
    """Najde najugodnejše avte glede na napoved modela."""

    avti = preberi_podatke(pot, na_voljo=True)

    X, y = pripravi_matrike(avti)
    model = treniraj_model(X, y)

    top_vsi = najdi_podcenjene(avti, model, n=len(avti))

    # Vnes znamke
    znamke = sorted(set(v["znamka"] for v in avti))
    print("\nZnamke na voljo:")
    print(", ".join(znamke))

    while True:
        znamka = input("\nZnamka (pusti prazno za brez filtra): ").strip().lower()

        if znamka == "":
            break

        if znamka in znamke:
            break

        # neveljavna znamka
        print(f"Znamka '{znamka}' ni med razpoložljivimi.")
        print("Poskusi eno izmed:")
        print(", ".join(znamke))

    # Vnes cene
    min_cena = input("Minimalna cena: ").strip()
    max_cena = input("Maksimalna cena: ").strip()

    min_cena = int(min_cena) if min_cena else None
    max_cena = int(max_cena) if max_cena else None

    # Upoštevanje izbire vnosa
    filtrirani = []
    for v in top_vsi:
        if znamka and v["znamka"] != znamka:
            continue
        if min_cena is not None and v["cena"] < min_cena:
            continue
        if max_cena is not None and v["cena"] > max_cena:
            continue
        filtrirani.append(v)

    if not filtrirani:
        print("\nNi vozil, ki ustrezajo filtrom.")
        return

    # Vnes števila rezultatov
    try:
        n = int(input("\nKoliko najugodnejših avtov želiš prikazati? "))
    except:
        n = 3

    # Izpis naj n najugodnejših avtov
    print("\nNajbolj podcenjeni avti:\n")
    for v in filtrirani[:n]:
        print(f"{v['naziv']}")
        print(f"  Cena: {v['cena']}")
        print(f"  Napoved: {v['napoved']:.0f}")
        print(f"  Razlika: {v['razlika']:.0f}")
        print(f"  Link: {v.get('link', '—')}\n")



#  Napoved cene za ročni vnos

def napovej_ceno(pot):
    """Napove ceno za ročni vnos podatkov o vozilu z modelom."""
    avti = preberi_podatke(pot)
    X, y = pripravi_matrike(avti)
    model = treniraj_model(X, y)

    print("\nVnesi podatke o vozilu:")
    letnik = int(input("Letnik: "))
    km = int(input("Prevoženi km: "))
    kw = int(input("Moč motorja (kW): "))

    starost = 2026 - letnik
    km_leto = km / starost if starost > 0 else km

    X_nov = [[km, kw, starost, km_leto]]
    napoved = model.predict(X_nov)[0]

    print(f"\nNapovedana cena: {napoved:.0f} €")


def povzetek_podatkov(pot):
    """Izpiše osnovne statistike o podatkih, kot so število avtov, znamke, prodani/na voljo."""
    avti = preberi_podatke(pot, False)

    # Avti na voljo (tisti, ki imajo ceno)
    na_voljo = [a for a in avti if a["cena"] is not None]

    # Prodani avti
    prodani = [a for a in avti if a["prodano"]]

    # Znamke
    znamke = sorted(set(a["znamka"] for a in avti))

    print("---Povzetek podatkov:---")
    print(f"Skupno število avtov: {len(avti)}")
    print(f"Na voljo za nakup:    {len(na_voljo)}")
    print(f"Prodani:              {len(prodani)}")
    print("\nZnamke v podatkih:")
    print(", ".join(znamke))
    print("\n")

# Glavni meni

def main():
    os.makedirs(MAPA_ARHIV, exist_ok=True)

    print("\n---Izberi podatke za delo---")
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

   # Izpis povzetka podatkov
    povzetek_podatkov(pot)

    # Glavni meni po izbiri podatkov
    while True:
        print("---Kaj želiš narediti?---")
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
            analiza_UV(pot)

        elif izbira == "4":
            print("Izhod.")
            break

        else:
            print("Neveljavna izbira.")

if __name__ == "__main__":
    main()
