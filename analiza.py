import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

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
    
    #filtrirani = [
    #    v for v in data
    #    if v.get("cena") and v.get("km")
    #]

    return data


   
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

    zaloga_po_znamkah = Counter(v['znamka'] for v in avti if not v.get('prodano'))
    goriva = Counter(v['gorivo'] for v in avti)
    prodani_po_znamkah = Counter(v['znamka'] for v in avti if v.get('prodano'))

    return zaloga_po_znamkah, prodani_po_znamkah, goriva

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

def najpogostejsi_model_in_avti(avti, ime_znamke):
    '''Vrne seznam avtomobilov za najpogostejši model izbrane znamke.'''

    modeli = []
    pari = []

    ime_znamke_lower = ime_znamke.lower()

    for avto in avti:
        znamka = avto.get('znamka', '').lower()
        naziv = avto.get('naziv', '')
        # Preverimo, ali se znamka ujema in ali naziv obstaja
        if znamka != ime_znamke_lower or not naziv:
            continue

        naziv_lower = naziv.lower()
        # Če naziv začne z imenom znamke, odstranimo ta del, sicer vzamemo cel naziv
        if naziv_lower.startswith(ime_znamke_lower):
            ostanek = naziv[len(ime_znamke):].strip()
        else:
            ostanek = naziv.strip()

        deli = ostanek.split()
        if not deli:
            continue
        
        model = deli[0].lower()   

        modeli.append(model)
        pari.append((model, avto))

    if not modeli:
        return []
    # Poiščemo najpogostejši model
    naj_model = Counter(modeli).most_common(1)[0][0]

    return [avto for m, avto in pari if m == naj_model]

def izlusci_znamko(vsi_avti, ime_znamke):
    '''Iz seznama vseh vozil vrne samo vozila določene znamke.'''
    return [
        v for v in vsi_avti 
        if v.get('znamka', '').lower() == ime_znamke.lower()
    ]



# =========VISUALIZACIJA========

def indikatorji(avti_znamke):
    '''Izračuna ključne indikatorje.'''
    
    neprodani = [
        v for v in avti_znamke 
        if not v.get('prodano') and v.get('cena') and v.get('km') and v.get('letnik')
    ]
    
    if not neprodani:
        return 'Za to znamko ni zaloge'

    stevilo = len(neprodani)
    povp_cena = sum(v['cena'] for v in neprodani) / stevilo
    povp_km = sum(v['km'] for v in neprodani) / stevilo
    povp_letnik = sum(v['letnik'] for v in neprodani) / stevilo

    return {
        'stevilo': stevilo,
        'povp_cena': round(povp_cena),
        'povp_km': round(povp_km),
        'povp_letnik': round(povp_letnik)
    }


# ___najugodnejši avtomobil___
def najugodnejse(avti, znamka = None):
    '''Poišče neprodan avtomobil z najboljšim razmerjem cena/km.'''

    neprodani_avti = [
        v for v in avti
        if not v.get('prodano') and v.get('cena') and v.get('km')
    ]

    if znamka:
        neprodani = izlusci_znamko(neprodani_avti, znamka)
    else:
        neprodani = neprodani_avti

    if not neprodani:
        return None
    
    best = min(neprodani, key = lambda v: v['cena'] / v['km'])

    return {
        'naziv': best.get('naziv'),
        'cena': best.get('cena'),
        'letnik': best.get('letnik'),
        'km': best.get('km'),
        'prostornina': best.get('prostornina'),
        'kw': best.get('kw'),
        'link': best.get('link'),
    }
    

# ___zaloga znamk___

def graf_zaloga_znamk(axs, zaloga_po_znamkah):
    '''Nariše stolpčni diagram števila vozil posamezne znamke na zalogi.'''
    if not zaloga_po_znamkah:
        axs.set_title('Ni podatkov o zalogi')
        axs.axis('off')
        return
    
    razvrsceno = sorted(zaloga_po_znamkah.items(), key = lambda x: x[1], reverse=True)
    imena = [x[0] for x in razvrsceno]
    kolicine = [x[1] for x in razvrsceno]
    axs.bar(imena, kolicine, color='blue', edgecolor='black')

    axs.set_title('Število vozil na zalogi', fontsize=14, fontweight='bold')
    axs.set_ylabel('Število vozil')
    axs.tick_params(axis='x', rotation=90) # Obrnemo imena znamk, da se ne prekrivajo
    axs.grid(axis='y', linestyle='--', alpha=0.7)


def slika_zaloge_znamk(datoteka):
    '''Ustvari sliko zalogo avtomobilov po znamkah.'''
    podatki = pripravi_podatke(datoteka)
    zaloga_po_znamkah, _, _ = statistika(podatki)

    fig, ax = plt.subplots(figsize=[8, 6])

    graf_zaloga_znamk(ax, zaloga_po_znamkah)

    plt.tight_layout()
    plt.show()


# ___prodaja znamk___
def graf_prodane_znamke(ax, prodani_po_znamkah):
    '''Nariše stolpčni diagram števila prodanih vozil posamezne znamke.'''
    if not prodani_po_znamkah:
        ax.set_title('Ni podatkov o prodanih vozilih')
        ax.axis('off')
        return

    # Sortiramo od največ prodanih do najmanj
    razvrsceno = sorted(prodani_po_znamkah.items(), key=lambda x: x[1], reverse=True)
    imena = [x[0] for x in razvrsceno]
    kolicine = [x[1] for x in razvrsceno]

    ax.bar(imena, kolicine, color='green', edgecolor='black')

    ax.set_title('Število prodanih vozil po znamkah', fontsize=14, fontweight='bold')
    ax.set_ylabel('Število prodanih')
    ax.tick_params(axis='x', rotation=90)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

def slika_prodanih_znamk(datoteka):
    '''Upravitelj, ki samostojno prebere podatke, odpre okno in nariše graf prodanih vozil.'''

    podatki = pripravi_podatke(datoteka)
    _, prodani_po_znamkah, _ = statistika(podatki)

    fig, ax = plt.subplots(figsize=[8, 6])

    graf_prodane_znamke(ax, prodani_po_znamkah)

   
    plt.tight_layout()
    plt.show()

# __GORIVA___
def graf_goriva(ax, goriva):
    '''Nariše tortni diagram razmerja goriv.'''
    if not goriva:
        ax.set_title('Ni podatkov o gorivih')
        ax.axis('off')
        return

    oznake = list(goriva.keys())
    vrednosti = list(goriva.values())

    barve = ['green', 'blue', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta'][:len(oznake)]

    ax.pie(
        vrednosti, 
        labels=oznake, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=barve[:len(oznake)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )

    ax.set_title('Razmerje goriv na trgu', fontsize=14, fontweight='bold')
    ax.axis('equal')  

def slika_goriv(datoteka, znamka = None):
    '''nariše tortni diagram goriv.'''
    vsi_avti = pripravi_podatke(datoteka)
        
    if znamka:
        avti = izlusci_znamko(vsi_avti, znamka)
    else:
        avti = vsi_avti
    
    _, _, goriva = statistika(avti)
    
    fig, ax = plt.subplots(figsize=[8, 6])
    graf_goriva(ax, goriva)
    plt.tight_layout()
    plt.show()


# ___ANALIZA MODELA (Cena vs KM)___

def graf_cena_km(ax, vozila, naslov_modela):
    podatki = [
        (v['km'], v['cena'], v['letnik'])
        for v in vozila
        if not v.get('prodano')
        and (v.get('km') or 0) > 0
        and (v.get('cena') or 0) > 0
        and v.get('letnik')
    ]

    if not podatki:
        ax.set_title(f'Ni podatkov za {naslov_modela}')
        ax.axis('off')
        return

    km, cene, letniki = zip(*podatki)

    scatter = ax.scatter(km, cene, c = letniki, cmap = 'viridis')

    plt.colorbar(scatter, ax = ax)

    ax.set_title(naslov_modela)
    ax.set_xlabel('km')
    ax.set_ylabel('cena')

    ax.grid(True)


def slika_analiza_modela(datoteka, ime_znamke):
    '''nariše graf cene glede na kilometre za najpogostejši model določene znamke.'''
    
    vsi_avti = pripravi_podatke(datoteka)
    vozila_modela = najpogostejsi_model_in_avti(vsi_avti, ime_znamke)
    
    if not vozila_modela:
        print(f"Za znamko {ime_znamke} nismo našli podatkov.")
        return
    
    prvi_avto = vozila_modela[0]
    naziv = prvi_avto.get('naziv', '')
    
    ime_modela = naziv.split()[1] if len(naziv.split()) > 1 else "Model"

    
    fig, ax = plt.subplots(figsize=[10, 7])

    graf_cena_km(ax, vozila_modela, f"{ime_znamke} {ime_modela}")

    # 4. Prikaz
    plt.tight_layout()
    plt.show()
    
    prvi_avto = vozila_modela[0]
    naziv = prvi_avto.get('naziv', '')
    ime_modela = naziv.split()[1] if len(naziv.split()) > 1 else "Model"

    fig, ax = plt.subplots(figsize=[10, 7])

    graf_cena_km(ax, vozila_modela, f"{ime_znamke} {ime_modela}")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ime_datoteke = "span_avti_23-04-2026.json"
    
    
    
    
    slika_zaloge_znamk(ime_datoteke)
    
    
    
    slika_prodanih_znamk(ime_datoteke)
    

    slika_goriv(ime_datoteke, znamka = 'volkswagen')

    vsi_avti = pripravi_podatke(ime_datoteke)
    
    
    slika_analiza_modela(ime_datoteke, 'volkswagen')