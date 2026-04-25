import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error


#Branje in filtriranje
def preberi_podatke(pot, na_voljo=True):
    """Prebere JSON datoteko in pripravi podatke za RF. Če na_voljo=True, izloči avte brez cene (prodane)."""
    with open(pot, "r", encoding="utf-8") as f:
        podatki = json.load(f)

    rezultat = []
    for v in podatki:
        if na_voljo and v.get("cena") is None:
            continue
        if v.get("km") is None:
            continue
        if v.get("letnik") is None:
            continue

        # preverjanje veljavnosti letnika
        letnik = v["letnik"]        
        if not isinstance(letnik, int):
            continue
        if letnik < 1990 or letnik > 2026:
            continue
        starost = 2026 - letnik
        km_leto = v["km"] / starost if starost > 0 else None

        v["starost"] = 2026 - v["letnik"]
        v["km_leto"] = km_leto

        rezultat.append(v)

    return rezultat


# Priprava X in y
def pripravi_matrike(avti):
    """Iz slovarjev pripravi matriko X in vektor y."""

    X = []
    y = []

    for v in avti:
        X.append([
        v["km"],
        v["kw"],
        v["starost"],
        v["km_leto"]])

        y.append(v["cena"])

    return X, y


# 3) Učenje modela
def treniraj_model(X, y):
    """Treniranje RF modela in izpis osnovne metrike."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, preds)

    print(f"MAPE: {mape * 100:.2f}%")

    return model


# 4) Iskanje podcenjenih avtov
def najdi_podcenjene(avti, model, n=3):
    """Doda napovedi in vrne najbolj podcenjene avte."""
    X, _ = pripravi_matrike(avti)
    preds = model.predict(X)

    for v, p in zip(avti, preds):
        v["napoved"] = p
        v["razlika"] = p - v["cena"]

    avti_sorted = sorted(avti, key=lambda v: v["razlika"], reverse=True)
    return avti_sorted[:n]



# 5) Glavni del
if __name__ == "__main__":
    datoteka = "data\\arhiv\\span_avti_22-04-2026.json"

    avti = preberi_podatke(datoteka)
    X, y = pripravi_matrike(avti)
    model = treniraj_model(X, y)

    top_min = najdi_podcenjene(avti, model)

    print("\nNajbolj podcenjeni avti:")
    for v in top_min:
        print(f"{v['naziv']}")
        print(f"  Cena: {v['cena']}")
        print(f"  Napoved: {v['napoved']:.0f}")
        print(f"  Razlika: {v['razlika']:.0f}")
        print(f"  Link: {v.get('link', '—')}")
        print()

    imena = ["km", "kw", "starost", "km_leto"]