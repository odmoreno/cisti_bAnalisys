
from ieeeObj import PaperInfo
from authorsObj import Author
from common_functions import *

import csv
import uuid

class ExtractData:
    def __init__(self):
        self.authorsDict = {}
        self.affiliationsDict = {}
        self.paisesxregion = load_generic('Data/paises.json')

    # Función para leer el archivo CSV, crear objetos y almacenarlos en un diccionario
    def leer_csv_y_crear_objetos_dict(self, archivo_csv, year):
        # Diccionario para almacenar los objetos
        objetos_dict = {}
        objetos_min = {}
        counterPaper = 0
        # Abrir el archivo CSV y leerlo
        with open(archivo_csv, mode='r', encoding='utf-8') as file:
            # Crear un lector CSV
            reader = csv.DictReader(file)

            # Iterar sobre cada fila del archivo CSV
            for row in reader:
                id = year + '_' + str(counterPaper)
                # print(row['Document Title'])
                autores = row['Authors'].split(';')
                auAffs = row['Author Affiliations'].split(';')
                ieeterms = row['IEEE Terms'].split(';')
                authKeys = row['Author Keywords'].split(';')
                # Crear un objeto con los atributos de la fila actual
                objeto = PaperInfo(id, row['Document Title'], autores, auAffs, row['Publication Year'],
                                   row['Abstract'], row['ISSN'], row['ISBNs'], row['DOI'], row['PDF Link']
                                   , authKeys, ieeterms, row['Reference Count'], row['Article Citation Count'],
                                   row['Publisher'])

                todict = objeto.to_dict()
                '''
                # Generar una clave aleatoria para el objeto basada en el DOI si está presente
                clave = str(uuid.uuid4())
                if 'DOI' in row:
                    clave = str(uuid.uuid5(uuid.NAMESPACE_DNS, row['DOI']))
                '''
                # Almacenar el objeto en el diccionario usando la clave generada
                objetos_dict[id] = todict
                #Obtener papers min
                newAuthors = self.obtener_autores_estructurados(autores, auAffs, year)
                objeto.set_new_authors(newAuthors)
                dictmin = objeto.dict_min()
                #Almacenar en el dict min
                objetos_min[id] = dictmin
                counterPaper += 1

        # Retornar el diccionario de objetos
        return objetos_dict, objetos_min

    def obtener_autores_estructurados(self, autores, affiliaciones, year):
        # Crear una lista de objetos Author
        authors_objects = []
        for name, affiliation in zip(autores, affiliaciones):
            # Dividir la afiliación en provincia (prov) y país
            affiliation_parts = affiliation.split(', ')
            nameAff = affiliation[0]
            prov = affiliation_parts[1]
            country = affiliation_parts[2]
            paisObject = self.paisesxregion[country.lower()]

            author = Author(name, prov, paisObject['country'], paisObject['continent'])
            author.create_aff_object(nameAff, year)
            todict = author.to_dict()
            authors_objects.append(todict)

        return authors_objects