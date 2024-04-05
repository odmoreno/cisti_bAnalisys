'''
funciones para sacar cocitationes
'''

from common_functions import *


class PapersData:
    def __init__(self):
        self.papers = {}
        self.coauthors = {}
        self.coauth_aff = {}
        self.coauth_regions = {}
        self.coauth_countries = {}

        self.authors_acum = {}
        self.countries_acum = {}
        self.aff_acum = {}

        self.datapath = 'Coauthor/'

        self.authors = load_generic('authors.json')
        self.universities = load_generic('../data/affiliations.json')
        self.affiliations_old = load_generic('../data/affiliations.json')

        self.current_doi = ''
        self.last_doi = ''
        self.conferences = {
            1: 'ejla',
            2: 'elak',
            3: 'elas'
        }

        self.bannedNames = ['', 'NA', ' NA']

    def loop_papers(self, papers, count=0):
        for id, data in papers.items():
            self.current_doi = id

            self.get_coauthors_people(data, count)
            self.get_coauthors_institutes(data, count)
            self.get_coauthors_regions(data, count)
            self.get_coauthors_countries(data, count)

    def mintext(self, element):
        return element.replace(' ', '').lower()

    def get_keys_for_dict(self, r1, r2, year):
        codid = r1 + ':' + r2 + ':' + year
        icodid = r2 + ':' + r1 + ':' + year
        uuid = r1 + ':' + r2
        uuiid = r2 + ':' + r1
        return codid, icodid, uuid, uuiid

    def save_data_in_dict(self, e1, e2, attribute ,year, codid, uuid, uuiid, dict_original, dict_acum):
        data = {
            'source': e1[attribute],
            'target': e2[attribute],
            'year': year,
            'weight': 1,
            'total': 0,
        }
        dict_original[codid] = data
        '''regular el total por year'''
        total = self.get_total_acum( uuid, uuiid, dict_acum, data['weight'] )
        dict_original[codid]['total'] = total
        return codid

    def get_coauthors_countries(self, data, count):
        authors = data['authors']
        year = str(data['year'])
        selfref = False
        for i, auth in enumerate(authors):
            if len(auth['affiliations']) > 0:
                afiliacion = auth['affiliations']
                affname = afiliacion['name']
                if affname != '':
                    r1 = self.mintext(afiliacion['country'])
                    if r1 == "netherlands":
                        print("ojo")
                    for j in range(i + 1, len(authors)):
                        auth2 = authors[j]
                        if len(auth2['affiliations']) > 0:
                            afiliacion2 = auth2['affiliations']
                            affname2 = afiliacion2['name']
                            if affname2 != '':
                                r2 = self.mintext(afiliacion2['country'])
                                if r1 != '' and r2 != '':
                                    codid, icodid, uuid, uuiid = self.get_keys_for_dict(r1, r2, year)
                                    if not self.country_exists(codid, icodid):
                                        codid = self.save_data_in_dict(afiliacion, afiliacion2, 'country',  year, codid, uuid, uuiid, self.coauth_countries, self.countries_acum)
                                        pais = self.coauth_countries[codid]
                                        if r1 == r2:
                                            selfref = True
                                    else:
                                        if r1 != r2:
                                            idcod = self.check_element_in_collection(codid, icodid,self.coauth_countries)
                                            total = self.update_acum(uuid, uuiid, self.countries_acum)
                                            self.coauth_countries[idcod]['total'] = total
                                        else:
                                            print('acum')
                                            if not selfref:
                                                idcod = self.check_element_in_collection(codid, icodid,self.coauth_countries)
                                                total = self.update_acum(uuid, uuiid, self.countries_acum)
                                                self.coauth_countries[idcod]['total'] = total
                                                selfref = True

    def get_coauthors_regions(self, data, count):
        authors = data['authors']
        year = str(data['year'])
        for i, auth in enumerate(authors):
            if len(auth['affiliations']) > 0:
                afiliacion = auth['affiliations']
                affname = afiliacion['name']
                if affname != '':
                    r1 = afiliacion['region'].replace(' ', '').lower()
                    for j in range(i + 1, len(authors)):
                        auth2 = authors[j]
                        if len(auth2['affiliations']) > 0:
                            afiliacion2 = auth2['affiliations']
                            affname2 = afiliacion2['name']
                            if affname2 != '':
                                r2 = afiliacion2['region'].replace(
                                    ' ', '').lower()
                                if r1 != '' and r2 != '':
                                    codid = r1 + ':' + r2 + ':' + year
                                    icodid = r2 + ':' + r1 + ':' + year
                                    if not self.region_exists(codid, icodid):
                                        data = {
                                            'source': afiliacion['region'],
                                            'target': afiliacion2['region'],
                                            'year': year,
                                            'weight': 1,
                                            'total': 1
                                        }
                                        self.coauth_regions[codid] = data
                                    else:
                                        if r1 != r2:
                                            self.check_element_in_collection(
                                                codid, icodid, self.coauth_regions)

    def get_coauthors_institutes(self, data, count):
        authors = data['authors']
        year = str(data['year'])
        selfref = False
        for i, auth in enumerate(authors):
            if len(auth['affiliations']) > 0:
                afiliacion = auth['affiliations']
                affname = afiliacion['name']
                if affname != '':
                    c1 = afiliacion['code']
                    for j in range(i + 1, len(authors)):
                        auth2 = authors[j]
                        if len(auth2['affiliations']) > 0:
                            afiliacion2 = auth2['affiliations']
                            affname2 = afiliacion2['name']
                            if affname2 != '':
                                c2 = afiliacion2['code']
                                if c1 != '' and c2 != '' and c1 != c2:
                                    codid, icodid, uuid, uuiid = self.get_keys_for_dict(c1, c2, year)
                                    # if (codid not in self.coauth_aff) and (icodid not in self.coauth_aff):
                                    if not self.insti_exists(codid, icodid):
                                        codid = self.save_data_in_dict(afiliacion, afiliacion2, 'name', year, codid, uuid,
                                                                       uuiid, self.coauth_aff,
                                                                       self.aff_acum)
                                        pais = self.coauth_aff[codid]
                                        if c1 == c2:
                                            selfref = True
                                    else:
                                        if c1 != c2:
                                            idcod = self.check_element_in_collection(codid, icodid,
                                                                                     self.coauth_aff)
                                            total = self.update_acum(uuid, uuiid, self.aff_acum)
                                            self.coauth_aff[idcod]['total'] = total
                                        else:
                                            print('acum')
                                            if not selfref:
                                                idcod = self.check_element_in_collection(codid, icodid,
                                                                                         self.coauth_aff)
                                                total = self.update_acum(uuid, uuiid, self.aff_acum)
                                                self.coauth_aff[idcod]['total'] = total
                                                selfref = True

    def get_coauthors_people(self, data, count):
        authors = data['authors']
        year = str(data['year'])
        for i, auth in enumerate(authors):
            a1 = auth['id']
            if a1 == "":
                continue
            for j in range(i + 1, len(authors)):
                auth2 = authors[j]
                a2 = auth2['id']
                if a2 == "":
                    continue

                if a1 != a2:
                    codid = a1 + ':' + a2 + ':' + year
                    icodid = a2 + ':' + a1 + ':' + year
                    uuid = a1 + ':' + a2
                    uuiid = a2 + ':' + a1
                    if not self.author_exists(codid, icodid):
                        data = {
                            'source': auth['id'],
                            'target': auth2['id'],
                            'year': year,
                            'weight': 1,
                            'total': 0,
                        }
                        self.coauthors[codid] = data
                        '''regular el total por year'''
                        total = self.get_total_acum(uuid, uuiid, self.authors_acum, data['weight'])
                        self.coauthors[codid]['total'] = total
                    else:
                        idcod = self.check_element_in_collection(codid, icodid, self.coauthors)
                        '''actualizar el total'''
                        total = self.update_acum(uuid, uuiid, self.authors_acum)
                        self.coauthors[idcod]['total'] = total
                        '''
                        if idcod == codid:
                            peso = self.coauthors[codid]['weight']
                            total = self.update_total(uuid, self.authors_acum, peso)
                            self.coauthors[codid]['total'] = total
                        elif idcod == icodid:
                            peso = self.coauthors[icodid]['weight']
                            total = self.update_total(uuiid, self.authors_acum, peso)
                            self.coauthors[icodid]['total'] = total
                        else:
                            print("error check")
                        '''

    def update_total(self, cod, elements, weight):
        if cod in elements:
            elements[cod] += 1
            return elements[cod]
        else:
            print(f"lampara")

    def update_acum(self,codid, icodid, elements):
        if codid in elements:
            elements[codid] += 1
            return elements[codid]
        if icodid in elements:
            elements[icodid] += 1
            return elements[icodid]

    def get_total_acum(self, codid, icodid, elements, weight):
        if not self.check_acum(codid,icodid, elements):
            elements[codid] = weight
            return elements[codid]
        else:
            if codid in elements:
                elements[codid] += weight
                return elements[codid]
            if icodid in elements:
                elements[icodid] += weight
                return elements[icodid]

    def check_element_in_collection(self, codid, icodid, elements):
        print(f"iD: {codid}")
        if codid in elements:
            print(f"el: {elements[codid]}")
            elements[codid]['weight'] += 1
            return codid
        if icodid in elements:
            print(f"e2l: {elements[icodid]}")
            elements[icodid]['weight'] += 1
            return icodid

    def region_exists(self, codid, icodid):
        # if (codid not in self.coauthors) and (icodid not in self.coauthors):
        return codid in self.coauth_regions or icodid in self.coauth_regions

    def country_exists(self, codid, icodid):
        # if (codid not in self.coauthors) and (icodid not in self.coauthors):
        return codid in self.coauth_countries or icodid in self.coauth_countries

    def insti_exists(self, codid, icodid):
        # if (codid not in self.coauthors) and (icodid not in self.coauthors):
        return codid in self.coauth_aff and icodid in self.coauth_aff

    def author_exists(self, codid, icodid):
        # if (codid not in self.coauthors) and (icodid not in self.coauthors):
        return codid in self.coauthors or icodid in self.coauthors

    def check_acum(self, codid, icodid, elements):
        return codid in elements or icodid in elements

    def clear_papers(self):
        self.papers = {}
        self.coauthors = {}
        self.coauth_aff = {}
        self.coauth_countries = {}
        self.coauth_regions = {}

    def generate_files_coauthors(self, path, cols, dict):
        csv_generics(path, dict.values(), cols)

    def get_affialition_info(self, aff):
        if aff in self.universities:
            return self.universities[aff]
        else:
            return self.affiliations_old[aff]

    def check_year(self, data, year, peso):
        if year not in data["years"]:
            data["years"][year] = peso

    def get_acum_weights(self, elements):
        new_elements = {}
        for key, data in elements.items():
            source = data['source']
            target = data['target']
            year = data['year']
            weight = data['weight']
            newid = source+":"+target
            if newid not in new_elements:
                data = {
                    'id': newid,
                    'total': 0,
                    'years': {}
                }
                self.check_year(data, year, weight)


    def loop_conferences(self, path1, conference_data):
        papersWC = conference_data
        cols = ['source', 'target', 'year', 'weight', 'total']
        path1_authors = self.datapath + path1 + "_Coauthorship_by_people.csv"
        path1_insti = self.datapath + path1 + "_Coauthorship_by_insti.csv"
        path1_region = self.datapath + path1 + "_Coauthorship_by_region.csv"
        path1_country = self.datapath + path1 + "_Coauthorship_by_countries.csv"
        for path in [path1_authors, path1_insti, path1_region, path1_country]:
            check_if_file_exist(path, file_type='csv')

        count = 1
        for papers in [papersWC]:
            # self.clear_papers()
            self.loop_papers(papers)

            '''generar csv'''
            self.generate_files_coauthors(path1_authors, cols, self.coauthors)
            self.generate_files_coauthors(
                path1_insti, cols, self.coauth_aff)
            self.generate_files_coauthors(
                path1_region, cols, self.coauth_regions)
            self.generate_files_coauthors(
                path1_country, cols, self.coauth_countries)
            count += 1

        save_generic('authors.json', self.authors)

        generalAutors = self.datapath + 'Global_Coauthorship_by_people.csv'
        generalInsti = self.datapath + 'Global_Coauthorship_by_insti.csv'
        generalRegion = self.datapath + 'Global_Coauthorship_by_region.csv'
        generalCountries = self.datapath + 'Global_Coauthorship_by_country.csv'

        self.generate_files_coauthors(generalAutors, cols, self.coauthors)
        self.generate_files_coauthors(generalInsti, cols, self.coauth_aff)
        self.generate_files_coauthors(generalRegion, cols, self.coauth_regions)
        self.generate_files_coauthors(
            generalCountries, cols, self.coauth_countries)
