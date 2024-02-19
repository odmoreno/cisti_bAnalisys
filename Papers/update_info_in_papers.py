'''
Creacion de;
1 - Papers min
2 - raw_authors_list
3 - update_raw_list
'''

import re
import hashlib

from common_functions import *
from papers_info import *

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)
current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())


class UpdateData:

    def __init__(self):
        # WorldCist proceedings
        self.conference_url = "https://ieeexplore.ieee.org/xpl/conhome/1800076/all-proceedings"
        self.base_url = "https://ieeexplore.ieee.org/"
        self.datapath = 'Data/'
        # Papers path original
        self.papers = {}
        # Papers min path
        self.papersmin = {}
        self.current_year = 0

    def set_paramethers(self, paper_path, paperminpath, affiliations_path, auth_path):
        # Papers min path
        self.papers_min_path = paperminpath
        # Papers path original
        self.papers_path = paper_path
        # affiliations path
        self.affiliationmin_path = affiliations_path
        # aff path
        self.authors_path = auth_path
        # check papersmin
        check_if_file_exist(self.papers_min_path)
        self.papersmin = load_generic(self.papers_min_path)
        # check authors
        check_if_file_exist(self.authors_path)
        self.authors_set = load_generic(self.authors_path)
        # load papers
        self.papers = load_generic(self.papers_path)
        # load affi
        check_if_file_exist(self.affiliationmin_path)
        self.affiliationmin = load_generic(self.affiliationmin_path)


        self.full_unis = load_generic('../Data/full_universities.json')
        self.affiliationsCodes = load_generic('../Data/affiliations.json')
        self.countryCodes = load_generic('../Data/country_codes.json')
        self.paises_set = load_generic('../Data/paises.json')

    def check_papers(self):
        '''Funcion principal'''
        success = 0
        fail = 0
        for doi, items in self.papers.items():
            try:
                if doi == "10.1145/3615522.3615528":
                    print("check")

                authors_pyalex = items['authorsPyAlex']
                authors_sch = items['authors'] if 'authors' in items else []
                year = self.check_year(items)
                if 'title' not in items:
                    info_pyalex = search_in_pyalex(doi)
                    title = info_pyalex['title']
                    year = info_pyalex['publication_year']
                else:
                    title = items['title']
                key = hashlib.md5(doi.encode()).hexdigest()
                print(f" paper with DOI: {doi} has key: {key}")
                self.current_year = year
                if key not in self.papersmin:
                    authors_pyalex = self.get_id_semantic(authors_sch, authors_pyalex)
                    authors_new = self.loop_authors_in_paper(authors_pyalex, doi, year)
                    data = {
                        'id': key,
                        'doi': doi,
                        'title': title,
                        'year': year,
                        'authors': authors_new,
                    }
                    self.save_papers_min(data)
                    success += 1
                    print(f"success {success}")
                else:
                    # print("check")
                    string = "check"
                    success += 1
                    pass

            except Exception as e:
                fail +=1
                print(e)
                print(f"Paper with DOI {doi} not found. {e}")
                print(f"Fails {fail}")

        print(f"fin check_papers fails {fail} Success {success}")
    def loop_authors_in_paper(self, authorList, doi, year):
        '''Funcion complementaria'''
        # lista final a retornar
        authors = []
        for authorElement in authorList:
            authorInfo = authorElement['author']
            # institutions = authorElement['institutions']
            affiliations = self.check_institutions(authorElement, doi, year)
            dataAuthor = self.create_data_author(authorInfo, affiliations, authorElement)
            authors.append(dataAuthor)
        return authors

    def create_data_author(self, author, institutions, element):
        '''Funcion complementaria'''
        authorId = self.get_numbers_id(author['id'])
        schId = ''
        if 'id_sch' in element:
            schId = element['id_sch']

        data = {
            'id': authorId,
            'author_sch': schId,
            'name': author['display_name'],
            'affiliations': institutions
        }
        self.save_authors_in_conference(data)
        return data

    def check_institutions(self, author, doi, year):
        '''Funcion complementaria'''
        # primero revisar si hay instituciones
        affiliations = []
        authorId = self.get_numbers_id(author['author']['id'])
        try:
            institutions = author['institutions']
            if len(institutions) > 0:
                print("hay instituciones")
                for element in institutions:
                    insti = self.clasificar_data_affiliation(element, year)
                    # affiliations[insti['id']] = insti
                    affiliations.append(insti)
            else:
                print('Revisar la raw data')
                raw_aff_string_list = author['raw_affiliation_strings']
                if len(raw_aff_string_list) > 0:
                    # create data aff
                    insti = raw_aff_string_list[0]
                    datainsti = self.create_data_aff(
                        {'display_name': insti}, year)
                    # affiliations[datainsti['id']] = datainsti
                    affiliations.append(datainsti)
        except Exception as e:
            print(e)
            print(f"Paper with DOI {doi} institucion Error. {e}")
        return affiliations

    def clasificar_data_affiliation(self, element, year):
        '''Funcion complementaria'''
        if 'raw_affiliation_strings' in element:
            # data del segundo tipo obtenida por scrapping
            return self.data_del_segundo_tipo(element, year)
        else:
            # data normal
            insti = self.create_data_aff(element, year, _hasInsti=True)
            return insti

    def data_del_segundo_tipo(self, element, year):
        '''Funcion complementaria'''
        id = element['id']
        saveFlag = False
        if id == '':
            code = element['code']
            name = element['name']
            id = hashlib.md5(code.encode()).hexdigest()
            saveFlag = True
        else:
            instimin = self.affiliationmin[id]
            name = instimin['name']
            code = instimin['code']

        data = {
            'id': id,
            'code': code,
            'name': name,
            'country': element['country'],
            'region': element['region'],
            'year': year
        }
        if saveFlag:
            self.save_institutions(data)
        return data

    def create_data_aff(self, element, year, _hasInsti=False):
        '''Funcion complementaria'''
        numberId = ''
        code = ''
        name = ''
        country = ''
        region = ''
        is_in_pyAlex = False
        data = {}
        try:
            if 'id' in element:
                numberId = self.get_numbers_id(element['id'])
                is_in_pyAlex = True

            if numberId not in self.affiliationmin:
                backupInsti = self.find_institution(element['display_name'])
                if backupInsti != '':
                    code = backupInsti['code']
                    name = backupInsti['name']
                    country = backupInsti['country']
                    region = backupInsti['region']
                    if numberId == '':
                        numberId = code
                    if 'id' in backupInsti:
                        if backupInsti['id'] != "":
                            numberId = backupInsti['id']
                            is_in_pyAlex = True

                if _hasInsti:
                    name = element['display_name']
                    country = self.find_country_code(element['country_code'])
                    if country == "":
                        country = backupInsti['country']
                    region = self.paises_set[country.lower()]['continent']
                    if 'region' in backupInsti:
                        if backupInsti['region'] != '':
                            region = backupInsti['region']
                    self.save_institute_new(name, country, region)

            else:
                aff_in_pyalex = self.affiliationmin[numberId]
                code = aff_in_pyalex['code']
                name = aff_in_pyalex['name']
                country = aff_in_pyalex['country']
                region = aff_in_pyalex['region']
                is_in_pyAlex = True

            data = {
                'id': numberId,
                'code': code,
                'name': name,
                'country': country,
                'region': region,
                'year': year,
                'in_pyAlex': is_in_pyAlex
            }
            # numberId != code and
            if numberId != '':
                self.save_institutions(data)
            else:
                print("iguales, remover")
                if numberId in self.affiliationmin:
                    del self.affiliationmin[numberId]
                    save_generic(self.affiliationmin_path, self.affiliationmin)

        except Exception as e:
            print(e)
            print(f" Institucion Error. {numberId}")
        return data

    def find_institution(self, displayName):
        '''Funcion complementaria'''
        minName = displayName.lower()
        affcode = minName.replace(" ", "")
        uni = ''
        if affcode in self.affiliationsCodes:
            uni = self.affiliationsCodes[affcode]
            uni['type'] = 'affcode'
            return uni
        """
                if minName in self.full_unis:
            uni = self.full_unis[minName]
            uni['type'] = 'fullunis'
            return uni
        """
        # save new insti
        elements = minName.split(', ')
        if len(elements) > 0:
            university = elements[0]
            country = elements[-1]
            code = university.replace(" ", "")
            region = ''
            if code in self.affiliationsCodes:
                uni = self.affiliationsCodes[code]
                uni['new'] = 'True'
                return uni

            if country in self.paises_set:
                region = self.paises_set[country]['continent']
            uni = {
                "name": university,
                "fullname": minName,
                "country": country,
                "region": region,
                "code": code,
                "new": True,
                "id": ''
            }
            self.affiliationsCodes[code] = uni
            save_generic('../Data/affiliations.json', self.affiliationsCodes)
        else:
            print('check')
        return uni

    def save_institute_new(self, displayName, countryB, regionB):
        '''Funcion complementaria'''
        minName = displayName.lower()
        # save new insti
        elements = minName.split(', ')
        if len(elements) > 0:
            university = elements[0]
            country = elements[-1]
            code = university.replace(" ", "")
            region = ''
            if country in self.paises_set:
                region = self.paises_set[country]['continent']

            if countryB != "":
                country = countryB
            if regionB != "":
                region = regionB
            uni = {
                "name": university,
                "fullname": minName,
                "country": country,
                "region": region,
                "code": code,
                "new": True,
                "id": ''
            }
            if code not in self.affiliationsCodes:
                self.affiliationsCodes[code] = uni
                save_generic('../Data/affiliations.json',
                             self.affiliationsCodes)
            else:
                if country != "":
                    self.affiliationsCodes[code]['country'] = country
                if region != "":
                    self.affiliationsCodes[code]['region'] = region
                save_generic('../Data/affiliations.json',
                             self.affiliationsCodes)
        else:
            print('check')

    def get_numbers_id(self, input_string):
        '''Funcion secundaria'''
        numbers = re.findall(r'\d+', input_string)
        if numbers:
            result = ''.join(numbers)
            print(result)
            return result
        else:
            print("No numbers found in the input string.")
            return ''

    def check_year(self, items):
        '''Funcion secundaria'''
        if 'year' in items:
            return items['year']
        else:
            if "published" in items:
                if "date-parts" in items["published"]:
                    year = items["published"]["date-parts"][0]
                    return year[0]

    def get_id_semantic(self, schlist, pyualexlist):
        '''Funcion secundaria'''
        # Check if the lengths of the two lists are the same
        if len(pyualexlist) == len(schlist):
            for i in range(len(pyualexlist)):
                pyualexlist[i]['id_sch'] = schlist[i]['authorId']
        else:
            print("Authors lists are not the same length.")
        return pyualexlist

    def find_country_code(self, code):
        country = ''
        if code in self.countryCodes:
            return self.countryCodes[code]['name']
        return country

    def save_institutions(self, institution):
        '''Funcion secundaria'''
        if institution['id'] not in self.affiliationmin:
            self.affiliationmin[institution['id']] = institution
        else:
            if institution['country'] != '' and self.affiliationmin[institution['id']]['country'] != '':
                self.affiliationmin[institution['id']
                                    ]['country'] = institution['country']
            if institution['region'] != '' and self.affiliationmin[institution['id']]['region'] != '':
                self.affiliationmin[institution['id']
                                    ]['region'] = institution['region']

            anioAnterior = self.affiliationmin[institution['id']]['year']
            year = institution['year']
            if year > anioAnterior:
                self.affiliationmin[institution['id']]['year'] = year

        save_generic(self.affiliationmin_path, self.affiliationmin)

    def save_papers_min(self, element):
        if element['id'] not in self.papersmin:
            self.papersmin[element['id']] = element

        save_generic(self.papers_min_path, self.papersmin)

    def save_authors_in_conference(self, element):
        authorid = element['id']
        instis = element['affiliations']

        if authorid not in self.authors_set:
            self.authors_set[authorid] = element
        else:
            if len(instis) > 0:
                for insti in instis:
                    id_insti = insti['id']
                    self.add_or_replace_affiliation(authorid, insti, _hasYear=True, year=self.current_year)

        save_generic(self.authors_path, self.authors_set)

    def add_or_replace_affiliation(self, authorid, new_affiliation, _hasYear=False, year=0):
        if len(self.authors_set[authorid]['affiliations']) == 0:
            self.authors_set[authorid]['affiliations'].append(new_affiliation)
            return

        id_to_add = new_affiliation["id"]
        if _hasYear:
            year_to_add = year
        else:
            year_to_add = new_affiliation["year"]

        updated = True  # Flag to track whether the affiliation was added or replaced
        affs = self.authors_set[authorid]['affiliations']
        for i, affiliation in enumerate(self.authors_set[authorid]['affiliations']):
            if "id" in affiliation:
                if affiliation["id"] == id_to_add:
                    # If the ID matches, check the year
                    if year_to_add > affiliation["year"]:
                        # Replace the affiliation with the one having a higher year
                        self.authors_set[authorid]['affiliations'][i] = new_affiliation
                    updated = False

        if updated:
            self.authors_set[authorid]['affiliations'].append(new_affiliation)

    def save_authors_general(self):
        papers = load_generic('Data/papers_merge.json')
        self.authors_path = 'Data/autores.json'
        self.authors_set = {}

        current_year = 0
        for doi, paper in papers.items():

            if current_year != paper['year']:
                print(current_year)

            current_year = paper['year']
            autors_in_paper = paper['authors']

            for autor in autors_in_paper:
                autor_id = autor['id']
                autor_name = autor['name']
                autor_aff = autor['affiliations']
                self.save_authors_in_conference(autor, current_year)
