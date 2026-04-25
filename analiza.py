import matplotlib.pyplot as plt
from collections import Counter
from napovedni_model import preberi_podatke

id_znamk = {'audi':'3','bentley':'103','bmw':'4','citroen':'6','cupra':'128','fiat':'9','ford':'10',
            'jeep':'14','kia':'15','land rover':'18','mercedes-benz':'22','mini':'23','nissan':'25',
            'opel':'26','peugeot':'27','porsche':'29','renault':'31','seat':'34','skoda':'37','toyota':'38',
            'volkswagen':'40','volvo':'39'}

   
def analiza_znamk(avti):
    '''Analizira znamke avtomobilov in poišče najugodnejšo in najmanj ugodno znamko.'''
    indeksi = {}
    # Gremo čez vse avtomobile in izračunamo indeks cena/km za vsako znamko
    for v in avti:
        cena = v.get('cena') or 0
        km = v.get('km') or 0
        znamka = v.get('znamka')

        if not znamka or km <= 100 or cena <= 0:
            continue

        indeks = cena / km
        
        if znamka in indeksi:
            indeksi[znamka].append(indeks)
        else:
            indeksi[znamka] = [indeks]
            
    # Izračunamo povprečni indeks za vsako znamko
    povprecja = {z: sum(vr) / len(vr) for z, vr in indeksi.items()}

    return povprecja

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


def najpogostejsi_model_in_avti(avti, ime_znamke):
    '''Vrne seznam avtomobilov za najpogostejši model izbrane znamke.'''

    modeli = []
    pari = []

    ime_znamke = ime_znamke.lower()

    for avto in avti:
        znamka = avto.get('znamka', '').lower()
        naziv = avto.get('naziv', '')

        # filtriranje po znamki
        if znamka != ime_znamke or not naziv:
            continue

        naziv_lower = naziv.lower()

        # odstrani ime znamke iz naziva
        if naziv_lower.startswith(ime_znamke):
            ostanek = naziv_lower[len(ime_znamke):].strip()
        else:
            ostanek = naziv_lower.strip()

        deli = ostanek.split()
        if not deli:
            continue

        model = deli[0]

        modeli.append(model)
        pari.append((model, avto))

    if not modeli:
        return []

    najpogostejsi = Counter(modeli).most_common(1)[0][0]

    return [avto for m, avto in pari if m == najpogostejsi]


def izlusci_znamko(vsi_avti, ime_znamke):
    '''Iz seznama vseh vozil vrne samo vozila določene znamke.'''
    return [
        v for v in vsi_avti 
        if v.get('znamka', '').lower() == ime_znamke.lower()
    ]



# =========VISUALIZACIJA========

def slika_zaloge_znamk(datoteka):
    '''Ustvari in shrani poenostavljen graf zaloge.'''
    podatki = preberi_podatke(datoteka, na_voljo=False)    
    zaloga, _, _ = statistika(podatki)

    if not zaloga:
        return

    razvrsceno = sorted(zaloga.items(), key = lambda x: x[1], reverse=True)
    imena = [x[0] for x in razvrsceno]
    kolicine = [x[1] for x in razvrsceno]

    fig = plt.figure(figsize = [8, 6])
    plt.bar(imena, kolicine, color = 'blue')
    plt.title('Število vozil na zalogi')
    plt.xticks(rotation = 90)

    plt.tight_layout() 
    plt.show()
    plt.close()


def slika_prodanih_znamk(datoteka):
    '''Ustvari in shrani poenostavljen graf prodaje.'''
    podatki = preberi_podatke(datoteka, na_voljo=False)
    _, prodani, _ = statistika(podatki)

    if not prodani:
        return

    razvrsceno = sorted(prodani.items(), key = lambda x: x[1], reverse=True)
    imena = [x[0] for x in razvrsceno]
    kolicine = [x[1] for x in razvrsceno]

    fig = plt.figure(figsize = [8, 6])
    plt.bar(imena, kolicine, color = 'green')
    plt.title('Število prodanih vozil po znamkah')
    plt.xticks(rotation = 90)

    plt.tight_layout()
    plt.show()
    plt.close()


def slika_goriv(datoteka, znamka = None):
    '''Nariše osnovni tortni diagram goriv in ga shrani.'''
    vsi_avti = preberi_podatke(datoteka, na_voljo=False)
        
    if znamka:
        avti = izlusci_znamko(vsi_avti, znamka)
        naslov = f'Razmerje goriv: {znamka.capitalize()}'
    else:
        avti = vsi_avti
        naslov = 'Razmerje goriv na celotnem trgu'
    
    _, _, goriva = statistika(avti)
    if not goriva:
        return 'Ni podatkov o gorivih.'
    
    oznake = list(goriva.keys())
    vrednosti = list(goriva.values())

    fig = plt.figure(figsize=[8, 6])
    plt.pie(vrednosti, labels=oznake, autopct = '%1.1f%%')
    plt.title(naslov)
    
    plt.tight_layout()
    plt.show()
    plt.close()


def slika_analiza_modela(datoteka, ime_znamke):
    '''Nariše graf razpršenosti cene in km (z letniki).'''
    vsi_avti = preberi_podatke(datoteka, na_voljo=False)
    vozila = najpogostejsi_model_in_avti(vsi_avti, ime_znamke)
    
    if not vozila:
        return f'Za znamko {ime_znamke} nismo našli podatkov.'

    naziv = vozila[0].get('naziv', '')
    ime_modela = naziv.split()[1] if len(naziv.split()) > 1 else "Model"

    podatki = [
        (v['km'], v['cena'], v['letnik'])
        for v in vozila
        if not v.get('prodano')
        and (v.get('km') or 0) > 0
        and (v.get('cena') or 0) > 0
        and v.get('letnik')
    ]

    if not podatki:
        return f'Za model {ime_modela} znamke {ime_znamke} nismo našli dovolj podatkov za analizo.'

    # Razpakiramo vse tri komponente
    km, cene, letniki = zip(*podatki)

    fig = plt.figure(figsize=[8, 6])
    
    # Dodane barve glede na letnik
    scatter = plt.scatter(km, cene, c = letniki, cmap='viridis')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Letnik vozila')

    plt.title(f'Cena / km: {ime_znamke} {ime_modela}')
    plt.xlabel('Prevoženi kilometri')
    plt.ylabel('Cena')

    plt.tight_layout()
    plt.show()
    plt.close()

def slika_ugodnost_znamk(datoteka):
    '''Nariše stolpčni diagram ugodnosti znamk (indeks cena/km) od najdražje do najcenejše.'''
    vsi_avti = preberi_podatke(datoteka, na_voljo=False)
    
    povprecja = analiza_znamk(vsi_avti)
    
    if not povprecja:
        return 'Ni podatkov za analizo ugodnosti znamk.'

    razvrsceno = sorted(povprecja.items(), key = lambda x: x[1], reverse=True)
    imena = [x[0] for x in razvrsceno]
    vrednosti = [x[1] for x in razvrsceno]

    fig = plt.figure(figsize=[8, 6])
    plt.bar(imena, vrednosti, color = 'purple')
    
    plt.title('Povprečna cena na kilometer po znamkah')
    plt.ylabel('Indeks (€ / km)')
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.show()
    plt.close()


# test
if __name__ == '__main__':


    ime_datoteke = "data\\arhiv\\span_avti_22-04-2026.json"
    
    
    msg = slika_analiza_modela(ime_datoteke, 'mercedes-benz')
    if msg:
        print(msg)

    
    slika_zaloge_znamk(ime_datoteke)
    
    
    
    slika_prodanih_znamk(ime_datoteke)
    

    slika_goriv(ime_datoteke, znamka = 'audi')

    vsi_avti = preberi_podatke(ime_datoteke)
    
    
    

    povprecja = analiza_znamk(vsi_avti)
    for znamka, povprecje in povprecja.items():
        print(f"{znamka}: {povprecje:.2f} €/km")

    slika_ugodnost_znamk(ime_datoteke)
    
    slika_goriv(ime_datoteke)