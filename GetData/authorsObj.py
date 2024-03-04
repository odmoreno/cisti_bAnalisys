# Definir la clase para los autores

import uuid
import hashlib
from unidecode import unidecode

class Author:
    def __init__(self, name, country, region):
        self.name = name
        #self.prov = prov
        self.country = country
        self.region = region
        self.key = self.generate_key(self.name)
        self.hasMoreAff = False
        self.rawAff = []
        self.otherAff = ''

    def __repr__(self):
        return f"Author(name={self.name}, country={self.country}, region={self.region})"
    def generate_key(self, name):
        #key = f"{name_cleaned}_{unique_id}"
        # Convertir el nombre del autor a minúsculas y sin espacios
        sinacentoname = unidecode(name)
        name_cleaned = sinacentoname.lower().replace(' ', '')
        # Crear un objeto de resumen de mensaje MD5
        hasher = hashlib.md5()
        # Actualizar el objeto de resumen con el nombre del autor
        hasher.update(name_cleaned.encode())
        # Obtener el valor hash hexadecimal
        key = hasher.hexdigest()
        return key


    def create_aff_object(self, name, year):
        code = self.generate_key(name)
        codename = unidecode(name.replace(" ", "").lower())
        codename = ''.join(e for e in codename if e.isalnum())
        affiliation = {
            "id": code,
            "code": codename,
            "name": name,
            "country": self.country,
            "region": self.region,
            "year": year,
            "rawAff": self.rawAff
        }
        self.aff_object = affiliation

    def to_dict(self):
        return {
            'id': self.key,
            'name': self.name,
            'affiliations': self.aff_object,
            'hasMoreAff': self.hasMoreAff,
            'otherAff': self.otherAff,
            'rawAff': self.rawAff
        }

    def to_save(self):
        return {
            'id': self.key,
            'name': self.name,
            'affiliations': [self.aff_object]
        }