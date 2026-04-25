import json

with open("data\\arhiv\\span_avti_22-04-2026.json", encoding="utf-8") as f:
    avti = json.load(f)

znamke = [a["znamka"] for a in avti]
print(set(znamke))

aktivni = [a for a in avti if not a["prodano"]]
print(f"Število aktivnih avtov: {len(aktivni)}")

#majhni = [a for a in avti if a["cena"] and a["cena"] < 10000]
#print(f"Število avtov, ki stanejo manj kot 10.000 €: {len(majhni)}")
