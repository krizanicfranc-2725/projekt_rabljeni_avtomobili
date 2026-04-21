import json
import matplotlib.pyplot as plt
from collections import Counter

id_znamk = {
        'Audi': '3', 'Bentley': '103', 'BMW': '4', 'Citroën': '6', 'Citroen': '6', 
        'Cupra': '128', 'Fiat': '9', 'Ford': '10', 'Jeep': '14', 'Kia': '15', 
        'Land Rover': '18', 'Mercedes-Benz': '22', 'Mini': '23', 'Nissan': '25', 
        'Opel': '26', 'Peugeot': '27', 'Porsche': '29', 'Renault': '31', 
        'Seat': '34', 'Škoda': '37', 'Skoda': '37', 'Toyota': '38', 
        'Volkswagen': '40', 'Volvo': '39'
    }

def pripravi_podatke(datoteka):
    '''Pripravi podatke iz JSON datoteke in jih prefiltrira.'''
    with open(datoteka, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtrirani = [
        v for v in data
        if v.get("cena") and v.get("km") and v["cena"] >= 200 and v["km"] >= 20000
    ]

    return filtrirani

def najugodnejse(avti):
    '''Poišče avtomobil z najboljšim razmerjem cena/km.'''
    best = min(avti, key=lambda v: v['cena'] / v['km'])
    
    return {
        'naziv': best.get('naziv'),
        'indeks': best['cena'] / best['km'],
        'link': best.get('link')
    }
   
def analiza_znamk(avti):
    '''Analizira znamke avtomobilov in poišče najugodnejšo in najmanj ugodno znamko.'''
    indeksi = {}
    # Gremo čez vse avtomobile in izračunamo indeks cena/km za vsako znamko
    for v in avti:
        znamka = v['znamka']
        indeks = v['cena'] / v['km']
        
        if znamka in indeksi:
            indeksi[znamka].append(indeks)
        else:
            indeksi[znamka] = [indeks]
            
    # Izračunamo povprečni indeks za vsako znamko
    povprecja = {z: sum(vr) / len(vr) for z, vr in indeksi.items()}

    # Poiščemo znamko z najmanjšim in največjim povprečnim indeksom
    najugodnejsa = min(povprecja, key=povprecja.get)
    najslabsa = max(povprecja, key=povprecja.get)

    return povprecja, najugodnejsa, najslabsa

def statistika(avti):
    '''Analizira prodajo, zalogo in goriva.'''
    znamke = Counter(v['znamka'] for v in avti)
    goriva = Counter(v['gorivo'] for v in avti)
    prodani = Counter(v['znamka'] for v in avti if v.get('prodano'))

    naj_ponudba = znamke.most_common(1)[0]
    naj_prodani = prodani.most_common(1)[0] if prodani else (None, 0)

    return znamke, goriva, naj_ponudba, naj_prodani

def link_znamke(znamka):
    if znamka in id_znamk:
        return f'https://trgovina.span.si/sl/Rabljena-vozila/?znamka={id_znamk[znamka]}'
    return None




def xy(podatki, kljuc_x, kljuc_y):
    '''Izlušči pare (x, y) iz podatkov glede na podana ključa.'''
    x = []
    y = []
    
    for v in podatki:
        vr_x = v.get(kljuc_x)
        vr_y = v.get(kljuc_y)

        # Preverimo da sta oba podatka številki in večja od 0
        if vr_x is not None and vr_y is not None:
            x.append(vr_x)
            y.append(vr_y)

    return x, y

# =========VISUALIZACIJA========

def narisi_znamke(axs, povprecja):
    '''Nariše stolpčni graf povprečnih indeksov cena/km za znamke.'''
    razvrscene = sorted(povprecja.items(), key=lambda x: x[1], reverse=True)
    
    imena = [z[0] for z in razvrscene]
    vrednosti = [z[1] for z in razvrscene]

    axs.bar(imena, vrednosti, edgecolor = 'black')
    axs.set_title('Znamke: cena/km', fontsize = 15)
    axs.set_xlabel('Znamka')
    axs.set_ylabel('EUR/km')
    axs.tick_params(axis = 'x', rotation = 90)

def narisi_pie_goriva(axs, goriva):
    '''Nariše modern in pregleden tortni diagram na podano platno (ax).'''
    
    vrednosti = list(goriva.values())
    oznake = list(goriva.keys())
    
    barve = ['green', 'blue', 'red', 'orange', 'grey', 'purple', 'cyan', 'magenta'][:len(oznake)]  
    
    axs.pie(
        vrednosti,
        labels = oznake,
        colors = barve,               
        autopct = '%1.1f%%',               
    )
    
    axs.set_title('Razmerje goriv na trgu', fontsize = 15)
    axs.axis('equal')

