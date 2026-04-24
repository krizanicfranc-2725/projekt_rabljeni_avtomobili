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