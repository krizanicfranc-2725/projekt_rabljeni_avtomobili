class Avto:
    def __init__(self, id, naziv, znamka, gorivo, letnik, km, menjalnik, cena, cena_fin, prodano, prostornina, kw, km_motor):

        self.id = id
        self.naziv = naziv
        self.znamka = znamka
        self.gorivo = gorivo
        self.letnik = letnik
        self.km = km
        self.menjalnik = menjalnik
        self.cena = cena
        self.cena_fin = cena_fin
        self.prodano = prodano
        self.prostornina = prostornina
        self.kw = kw
        self.km_motor = km_motor


        self.link = f"https://trgovina.span.si/sl/Rabljena-vozila/Vozilo{id}/"

    def to_dict(self):
        return self.__dict__
    
    def eur_per_km(self):
        #vrne ceno na km, če imamo tako ceno kot kilometre, sicer None
        if self.cena is None or self.km is None or self.km == 0:
            return None
        return self.cena / self.km

