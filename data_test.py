import json

with open("span_avti_09-04-2026.json", encoding="utf-8") as f:
    avti = json.load(f)

znamke = [a["znamka"] for a in avti]
print(set(znamke))

aktivni = [a for a in avti if not a["prodano"]]
print(f"Število aktivnih avtov: {len(aktivni)}")