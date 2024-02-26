
from ieeeObj import PaperInfo
from authorsObj import Author
from common_functions import *

import csv
import uuid
import re

class ExtractData:
    def __init__(self):
        self.authorsDict = {}
        self.affiliationsDict = {}
        self.paisesxregion = load_generic('../Data/paises.json')

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
            try:
                # Dividir la afiliación en provincia (prov) y país
                affiliation_parts = affiliation.split(', ')
                affiliations = self.extract_universities(affiliation_parts)

                country = affiliation_parts[-1]
                paisObject = self.paisesxregion[country.lower()]

                author = Author(name, paisObject['country'], paisObject['continent'])
                author.create_aff_object(affiliations[0], year)
                author.rawAff = affiliations
                if len(affiliations) > 1:
                    print("tiene mas de 1")
                    author.hasMoreAff = True
                    author.otherAff = affiliations[1]

                todict = author.to_dict()
                authors_objects.append(todict)
            except Exception as e:
                print(e)


        return authors_objects

    def extract_universities(self, affiliation):
        # Expresión regular para buscar palabras relacionadas con "universidad" en varios idiomas
        regex = r"(?i)(\b(?:Universidad|University|Universidade|Universitat|Instituto|Polytechnic)\b[\w\s,']+)"
        matches = []
        for element in affiliation:
            word = re.findall(regex, element)
            match = re.search(regex, element)
            if len(word)>0:
                wordsito = match.group()
                matches.append(word[0])
        return matches


