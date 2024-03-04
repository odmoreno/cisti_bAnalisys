
from ieeeObj import PaperInfo
from authorsObj import Author
from common_functions import *

import csv
import uuid
import re

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())

class ExtractData:
    def __init__(self):
        self.authorsDict = {}
        self.affiliationsDict = {}
        self.mainPapers = {}
        self.paisesxregion = load_generic('../Data/paises.json')
        self.affiliations = load_generic('../Data/affiliations.json')
        self.backUPAffs = load_generic('Data/affiliations.json')

        self.prioridades = {
            "Universidad": 1,
            "University": 2,
            "Universidade": 3,
            "Universitat": 4,
            "Polytechnic": 5,
            "Politécnica": 5,
            "Instituto": 6,
            "Institute": 6,
            "Center": 7,
            "Centro": 7,
            "School": 8,
            "Escola": 9,
            "Department": 10,
            "Ministerio": 11,
            "Campus": 11,
        }

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
                # Almacenar el objeto en el diccionario usando la clave generada
                objetos_dict[id] = todict
                #Obtener papers min
                newAuthors = self.obtener_autores_estructurados(autores, auAffs, year)
                objeto.set_new_authors(newAuthors)
                dictmin = objeto.dict_min()
                #Almacenar en el dict min
                objetos_min[id] = dictmin
                #alamacenar en genearl
                self.mainPapers[id] = todict
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

                if len(affiliations) == 0:
                    print("OJO")
                    affiliations = [affiliation_parts[0]]
                if affiliations[0] == 'Universidad Nacional de Ingeniería':
                    print("check")

                country = self.check_country(affiliation) #affiliation_parts[-1]
                pais, region = self.check_pais_y_region(country)

                author = Author(name, pais, region)
                author.rawAff = affiliation.strip()
                author.create_aff_object(affiliations[0], year)

                if len(affiliations) > 1:
                    print("tiene mas de 1")
                    author.hasMoreAff = True
                    author.otherAff = affiliations[1]

                author = self.check_instutions_data(author)

                todict = author.to_dict()
                authors_objects.append(todict)

                self.check_author(author)
                self.check_institutions(author.aff_object)

            except Exception as e:
                print(e)
                author = Author(name, '', '')
                author.rawAff = affiliation

        return authors_objects

    def check_pais_y_region(self, country):
        pais = ''
        region = ''
        if country.lower() in self.paisesxregion:
            paisObject = self.paisesxregion[country.lower()]
            pais = paisObject['country']
            region = paisObject['continent']
        return pais, region


    def extract_universities(self, affiliation):
        # Expresión regular para buscar palabras relacionadas con "universidad" en varios idiomas
        # regex = r"(?i)(\b(?:Universidad|University|Universidade|Universitat|Instituto|Polytechnic|Center|School|Escola)\b[\w\s,']+)"
        regex = r"([^']*(?:Universidad|University|Universidade|Universitat|Instituto|Polytechnic|Politécnica|Institute|Center|Centro|School|Escola|Department|Ministerio|Campus)[^']*)"

        matches = []

        for element in affiliation:
           try:
               word = re.findall(regex, element)
               match = re.search(regex, element)
               if len(word) > 0:
                   cleanWord = word[0].strip()
                   wordsito = match.group()
                   matches.append(cleanWord)
           except Exception as e:
               print(f'error {e}')

        print("Matches sin ordenar:", matches)
        # Ordenar los matches según la prioridad de las palabras clave
        # matches.sort(key=lambda x: keyword_priority.get(re.findall(regex, x)[0], float('inf')))
        # Ordenar los matches según la prioridad de las palabras clave
        # matches.sort(key=lambda x: keyword_priority.get(x, float('inf')))

        lista_ordenada = self.ordenar_segun_prioridad(matches)

        print("Matches ordenados:", lista_ordenada)
        return lista_ordenada

    def ordenar_segun_prioridad(self, lista):
        # Diccionario de prioridad de palabras clave
        return sorted(lista, key=self.mi_criterio)

    def mi_criterio(self, item):
        for palabra, prioridad in self.prioridades.items():
            if palabra in item:
                return prioridad
        # Si ninguna palabra clave está presente, se coloca al final
        return len(self.prioridades) + 1

    def check_author(self, author):
        if author.key not in self.authorsDict:
            newelement = author.to_save()
            self.authorsDict[author.key] = newelement
        else:
            print('Author existe, check affs')
            # Mantener el orden de las afiliaciones y eliminar duplicados
            author_in_dict = self.authorsDict[author.key]
            current_author_aff = author.aff_object['code']
            not_exist = True
            for aff in author_in_dict['affiliations']:
                if current_author_aff == aff['code']:
                    not_exist = False

            if not_exist:
                self.authorsDict[author.key]['affiliations'].append(author.aff_object)

    def check_institutions(self, institution):
        if institution['code'] not in self.affiliationsDict:
            self.affiliationsDict[institution['code']] = institution


    def save_data(self):
        save_generic('Data/authors.json', self.authorsDict)
        save_generic('Data/affiliations2.json', self.affiliationsDict)


    def check_instutions_data(self, autor):
        institution = autor.aff_object
        code = institution['code']
        code2 = institution['name'].replace(" ", "").lower()
        idAff = institution['id']
        if institution['region'] == "":
            print("check")
            if idAff in self.backUPAffs:
                affBackup = self.backUPAffs[idAff]
                autor.aff_object['country'] = affBackup['country']
                autor.aff_object['region'] = affBackup['region']
            if code in self.affiliations:
                affBackup = self.affiliations[code]
                autor.aff_object['country'] = affBackup['country']
                autor.aff_object['region'] = affBackup['region']
            if code2 in self.affiliations:
                affBackup = self.affiliations[code2]
                autor.aff_object['country'] = affBackup['country']
                autor.aff_object['region'] = affBackup['region']

        if autor.aff_object['region'] == '':
            pais, region = self.check_pais_y_region(autor.aff_object['country'])
            autor.aff_object['country'] = pais
            autor.aff_object['region'] = region

        return autor

    def check_country(self, texto_largo):
        # Dividir el texto en palabras separadas
        palabras = texto_largo.split()
        paises_encontrados = []
        # Recorrer cada palabra y verificar si es un país
        for palabra in palabras:
            # Comprobar si la palabra está en el diccionario de países
            palabra = palabra.lower().strip()
            if palabra in self.paisesxregion:
                paises_encontrados.append(palabra)

        value = ""
        if len(paises_encontrados)>1:
            value = paises_encontrados[0]

        if len(paises_encontrados) == 1:
            print('no problem')
            value = paises_encontrados[0]


        return value