'''Funciones para hacer conteo '''

from common_functions import *
from counter import CountClient
from csv_generator import CsvGenerator

import os

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())


class RankMenu:

    def __init__(self):
        # WorldCist proceedings
        #self.conference_url = "https://link.springer.com/conference/worldcist"
        self.datapath = 'ranking/'
        # Data ha saber antes
        self.name_conf = ''
        self.papers_in_conference = {}
        # datos necesarios
        self.universities = load_generic('../Data/affiliations.json')
        self.affilitions_old = load_generic('../Data/affiliations.json')
        self.authors = load_generic('../GetData/Data/authorsU.json')
        # count client
        self.counterClient = CountClient()
        # Contadores globales
        self.global_authorCount = {}
        self.global_instiCount = {}
        self.global_countryCount = {}
        self.global_regionCount = {}

    def load_data_for_loop(self, path='../Papers/Data/papersmin4.json', name_conf='worldCist', years=[2017, 2018, 2019, 2020, 2021, 2022]):
        self.papers_in_conference = load_generic(path)
        self.name_conf = name_conf
        self.yearsList = years

    def loop_papers_in_conference(self):
        self.counterClient.reset_tmp_counts()

        for doi, paper in self.papers_in_conference.items():
            paperYear = paper['year']
            paperYear = int(paperYear)
            authors = paper['authors']
            self.loop_authors_per_paper(authors, paperYear)

        # mas por hacer aca
        print("next")
        sorted_authors = self.sort_elements(self.global_authorCount)
        sorted_insti = self.sort_elements(self.global_instiCount)
        sorted_regions = self.sort_elements(self.global_regionCount)
        sorted_countries = self.sort_elements(self.global_countryCount)
        # save
        save_generic(self.datapath + 'authors_count.json', sorted_authors)
        save_generic(self.datapath + 'affiliations_count.json', sorted_insti)
        save_generic(self.datapath + 'regions_count.json', sorted_regions)
        save_generic(self.datapath + 'country_count.json', sorted_countries)

    def loop_authors_per_paper(self, authors_in_paper, paperYear):
        # para revisar que no se repita
        tempAff = {}
        tempRegion = {}
        tempCountry = {}
        #Autores
        for author in authors_in_paper:
            if author['name'] == "":
                continue
            author_id = author['id']
            author_name = author['name']
            affiliation_info = author['affiliations']
            current_affiliation_id = affiliation_info['id']
            current_country = affiliation_info['country'].lower()
            current_region = affiliation_info['region'].lower()
            self.current_paper_year = paperYear
            # Registrar y contar Autores
            self.check_collections_and_count(
                author_id, author, affiliation_info, self.counterClient.tmp_author_count, self.create_data_general)
            if author_id not in self.global_authorCount:
                dataAutor = self.create_data_general(author, paperYear)
                dataAutor['country'] = current_country
                dataAutor['region'] = current_region
                self.global_authorCount[author_id] = dataAutor
            else:
                self.check_year(self.global_authorCount[author_id], paperYear)

            if current_country == "" or current_region == "" or affiliation_info['name'] == " NA":
                continue
            # Registrar y contar Afiliaciones
            self.check_collections_and_count(current_affiliation_id, affiliation_info,
                                             affiliation_info, self.counterClient.tmp_insti_count, self.create_data_general)
            #INstituciones
            if current_affiliation_id not in tempAff:
                if current_affiliation_id not in self.global_instiCount:
                    dataAffinfo = self.create_data_general(
                        affiliation_info, paperYear)
                    dataAffinfo['region'] = current_country
                    dataAffinfo['country'] = current_region
                    self.global_instiCount[current_affiliation_id] = dataAffinfo
                    self.check_conference(self.global_instiCount[current_affiliation_id])
                else:
                    self.check_conference(self.global_instiCount[current_affiliation_id])
                    self.check_year(
                        self.global_instiCount[current_affiliation_id], paperYear)
                # Registarr y contar paises
                self.check_collections_and_count(current_country, affiliation_info, affiliation_info,
                                                 self.counterClient.tmp_country_count, self.create_data_country,
                                                 isCountry=True)
                tempAff[current_affiliation_id] = 1

            # Paises
            if current_country not in tempCountry:
                if current_country not in self.global_countryCount:
                    dataCountry = self.create_data_country(affiliation_info, paperYear)
                    self.global_countryCount[current_country] = dataCountry
                    self.check_conference(self.global_countryCount[current_country])
                else:
                    self.check_conference(self.global_countryCount[current_country])
                    self.check_year(self.global_countryCount[current_country], paperYear)
                # Registarr y contar paises
                self.check_collections_and_count(current_region, affiliation_info, affiliation_info,
                                                 self.counterClient.tmp_region_count, self.create_data_region,
                                                 isRegion=True)
                tempCountry[current_country] = 1

            # Regiones
            if current_region not in tempRegion:
                if current_region not in self.global_regionCount:
                    dataReg = self.create_data_region(affiliation_info, paperYear)
                    self.global_regionCount[current_region] = dataReg
                    self.check_conference(self.global_regionCount[current_region])
                else:
                    self.check_conference(self.global_regionCount[current_region])
                    self.check_year(self.global_regionCount[current_region], paperYear)
                tempRegion[current_region] = 1

            #logout
            total = self.global_authorCount[author_id]['total']
            total_aff = self.global_authorCount[author_id]['total']
            print(f'Fin autor {author_name} con total de {total}')
            print(f'Fin aff {affiliation_info} con total de {total_aff}')
            print('_____________________________________________________')

    def check_collections_and_count(self, key, element, affiliation_info, collection, function, isCountry=False, isRegion=False):
        if key != "":
            if key not in collection:
                data = function(element, self.current_paper_year)
                if not isRegion:
                    if not isCountry:
                        data['country'] = affiliation_info['country']
                    data['region'] = affiliation_info['region']
                collection[key] = data
            else:
                self.check_year(collection[key], self.current_paper_year)

    def check_year(self, data, year):
        if year not in data["years"]:
            data["years"][year] = 1
        else:
            data["years"][year] += 1
        data["total"] += 1

    def create_data_general(self, element, year):
        data = {
            "id": element['id'],
            "name": element["name"],
            "total": 0,
            "years": {}
        }
        self.check_year(data, year)
        return data

    def create_data_country(self, data, year):
        country = data['country']
        region = data['region']
        data = {
            "id": country.replace(" ", "").lower(),
            "name": country,
            "region": region,
            "total": 0,
            "years": {}
        }
        self.check_year(data, year)
        return data

    def create_data_region(self, data, year):
        region = data['region']
        data = {
            "id": region,
            "name": region,
            "total": 0,
            "years": {}
        }
        self.check_year(data, year)
        return data

    def check_conference(self, element):
        if self.name_conf not in element:
            element[self.name_conf] = 1
        else:
            element[self.name_conf] += 1

    '''
    Sort package
    '''

    def sort_elements(self, elements):
        sorted_elements = dict(
            sorted(elements.items(), key=lambda x: x[1]['total'], reverse=True))
        sorted_elements = self.set_years_no_counted(sorted_elements)

        sorted_elements = self.sorted_years_ascendent(sorted_elements)
        return sorted_elements

    def set_years_no_counted(self, elements):
        for id, value in elements.items():
            for anio in self.yearsList:
                if anio not in value['years']:
                    elements[id]['years'][anio] = 0
            years_dict = elements[id]['years']
            # sorted_years = dict(sorted(years_dict.items(), key=lambda item: int(item[0]), reverse=True))
            # Sort the 'years' dictionary keys in descending order
            sorted_years_keys = sorted(
                years_dict.keys(), key=lambda x: int(x), reverse=True)
            # Create a new ordered dictionary with sorted keys
            sorted_years_dict = {key: years_dict[key]
                                 for key in sorted_years_keys}
            elements[id]['years'] = sorted_years_dict
        return elements

    def sorted_years_ascendent(self, sorted_elements):
        for id, values in sorted_elements.items():
            years = values['years']
            #sorted_years = dict(sorted(years.items()))
            sorted_years = dict(sorted(years.items()))
            sorted_elements[id]['years'] = sorted_years
            # print(sorted_elements[id]['years'])
        return sorted_elements

    def fill_region_authors(self, elements):
        for id, author in elements.items():
            affs = author['affiliations']

            mainAff = affs[0]
            tempRegion = mainAff['region']
            tempCountry = mainAff['country']
            tempAff = mainAff['name']

            elements[id]['country'] = tempCountry
            elements[id]['region'] = tempRegion
            elements[id]['affiliation'] = tempAff

        save_generic('authors.json', elements)
        return elements

    def save_authors(self, csv_file, merged_authors, columns):
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            # Crear un objeto escritor CSV
            writer = csv.writer(file)
            writer.writerow(columns)
            # Escribir los datos de cada autor y sus afiliaciones en el CSV
            for author_id, author_data in merged_authors.items():
                author_id = author_data["id"]
                name = author_data["name"]
                mainRegion = author_data["region"]
                mainCountry = author_data["country"]
                mainAff = author_data["affiliation"]
                affs = []
                countries = []
                regions = []
                # Escribir cada afiliación del autor en una fila separada
                for affiliation in author_data["affiliations"]:
                    affs.append(affiliation["name"])
                    countries.append(affiliation["country"])
                    regions.append(affiliation["region"])
                writer.writerow(
                    [author_id, name, affs, countries, regions, mainAff, mainCountry, mainRegion])

    def create_csv_authors(self, path='../Papers/Data/authors_info3.json'):
        columns = ["id", "name", "affiliations", "affiliation", "countries", "regions", "country", "region"]
        authors = load_generic(path)
        authors = self.fill_region_authors(authors)
        #self.save_authors('ranking_global_authors_per_conference.csv', authors, columns)
        self.save_authors('authors.csv', authors, columns)

    def create_csv_rankings(self):
        author_path_json = self.datapath + 'authors_count.json'
        aff_json_path = self.datapath + 'affiliations_count.json'
        country_json_path = self.datapath + 'country_count.json'
        region_json_path = self.datapath + 'regions_count.json'
        #csv paths
        author_csv = self.datapath + 'ranking_global_authors_per_year.csv'
        aff_csv = self.datapath + 'ranking_global_affilitations_per_year.csv'
        country_csv = self.datapath + 'ranking_global_countries_per_year.csv'
        region_csv = self.datapath + 'ranking_global_regions_per_year.csv'

        csvs = CsvGenerator()
        csvs.set_years_list(self.yearsList)

        csvs.create_csv_rankings(author_path_json, author_csv)
        csvs.create_csv_rankings(aff_json_path, aff_csv)
        csvs.create_csv_rankings(country_json_path, country_csv, _isCountry=True)
        csvs.create_csv_rankings(region_json_path, region_csv, _isRegion=True)

    '''Fin sort'''

    def generate_csv(self, papersPath):
        type = ""
        conference = 'Cisti'
        path = 'papers.csv'
        papers = load_generic(papersPath)
        newSet = {}
        for id, items in papers.items():
            try:
                list_of_authors = []
                list_of_affs = []
                list_of_countries = []
                list_of_regions = []
                doi = items['doi']
                for autor in items['authors']:
                    autorId = autor['id']
                    # autorElement = authors_set[autorId]
                    autorName = autor['name']
                    list_of_authors.append(autorName)

                    aff_info = autor['affiliations']
                    list_of_affs.append(aff_info['name'])

                    list_of_countries.append(aff_info['country'])
                    list_of_regions.append(aff_info['region'])

                data = {
                    'id': id,
                    'type': type,
                    'year': items['year'],
                    'title': items['title'],
                    'doi': doi,
                    'authors': list_of_authors,
                    'conference': conference,
                    'affiliations': list_of_affs
                }
                newSet[id] = data

            except Exception as e:
                print(e)

        list = ['id', 'type', 'year', 'title', 'doi', 'authors', 'countries', 'regions', 'conference', 'affiliations']
        csv_generics(path, newSet.values(), list)