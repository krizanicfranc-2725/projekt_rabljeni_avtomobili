from napovedni_model import preberi_podatke
from analiza import (
    slika_zaloge_znamk,
    slika_prodanih_znamk,
    slika_goriv,
    slika_ugodnost_znamk,
    slika_analiza_modela
)

def analiza_UV(pot):
    avti = preberi_podatke(pot, na_voljo=False)
    znamke = sorted(set(v["znamka"] for v in avti))

    while True:
        print("\n---ANALIZA TRGA – Izberi graf")
        print("1) Zaloga po znamkah")
        print("2) Prodani po znamkah")
        print("3) Graf goriv")
        print("4) Ugodnost znamk")
        print("5) Analiza najpogostejših modelov za izbrano znamko")
        print("6) Nazaj")

        izbira = input("\nIzberi možnost: ").strip()

        if izbira == "1":
            slika_zaloge_znamk(pot)

        elif izbira == "2":
            slika_prodanih_znamk(pot)

        elif izbira == "3":
            slika_goriv(pot)

        elif izbira == "4":
            slika_ugodnost_znamk(pot)

        elif izbira == "5":
            print("\nGraf prikazuje razmerje med ceno in kilometri za najpogostejši model izbrane znamke.")
            print("\nZnamke na voljo:")
            print(", ".join(znamke))

            while True:
                z = input("\nVnesi znamko (npr, volkswagen) ali Enter za izhod: ").strip().lower()

                if z == "":
                    print("Izhod iz analize modelov.")
                    break

                if z not in znamke:
                    print(f"Znamka '{z}' ni v podatkih. Poskusi znova.")
                    continue

                msg = slika_analiza_modela(pot, z)

                # Če funkcija vrne sporočilo
                if msg:
                    print(msg)

        elif izbira == "6":
            return

        else:
            print("Neveljavna izbira.")
