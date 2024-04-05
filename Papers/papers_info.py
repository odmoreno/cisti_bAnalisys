'''
Informacion de los papers por partes
'''

from common_functions import *
from paper_apis import *


class PapersInfo:

    def __init__(self):
        # WorldCist proceedings
        self.conference_url = "https://dblp.org/db/conf/vinci/index.html"
        self.base_url = "https://dl.acm.org/"
        self.datapath = 'Papers/Data/'

        self.proceeding_path = ''
        self.proocedings_list = {}
        # lista de datos a usar depues
        self.papers_set_path = 'Papers/Data/papers.json'
        self.papers_set = {}
        self.references_list_path = 'Papers/Data/ref_list.json'
        self.references = {}
        self.references_list = {}
        # Lista de nuevos papers

    def loop_proocedings(self, proocedings):
        check_if_file_exist(self.papers_set_path)
        self.papers_set = load_generic(self.papers_set_path)
        check_if_file_exist(self.references_list_path)
        self.references_list = load_generic(self.references_list_path)
        for key, value in proocedings.items():
            date = value['data_published']
            publisher = value['publisher']
            papers = value['papers']
            print(f' CISTI {date} pub: {publisher}')
            self.loop_papers_in_proocedings(papers)

    def loop_papers_in_proocedings(self, papers):

        for paper in papers:
            title = paper['title']
            doi = paper['doi']
            if doi not in self.papers_set:
                info = {}  #search_papers_sch(doi)
                info2 = {}  # search_in_crossref(doi)
                info3 = search_in_pyalex(doi)
                self.split_info_to_serve(doi, info, info2, info3)
                print(f'Fin {doi}')
                #save_generic(self.papers_set_path, self.papers_set)
                #save_generic(self.references_list_path, self.references_list)
            else:
                currentPaper = self.papers_set[doi]
                if 'authorsPyAlex' not in self.papers_set[doi]:
                    print("search")
                    pyalexInfo = search_in_pyalex(doi)
                    if 'authorships' in pyalexInfo:
                        self.papers_set[doi]['authorsPyAlex'] = pyalexInfo['authorships']
                else:
                    pyalaexauthors = currentPaper['authorsPyAlex']
                    '''
                                        if len(pyalaexauthors) == 0:
                        print(f"search again in {doi}")
                        pyalexInfo = search_in_pyalex(doi)
                        if 'authorships' in pyalexInfo:
                            self.papers_set[doi]['authorsPyAlex'] = pyalexInfo['authorships']
                    '''
                # abstract = self.reconstruir_abstract(doi, pyalexInfo, pyalexInfo['abstract_inverted_index'])
                # self.papers_set[doi]['abstract'] = abstract
                # self.papers_set[doi]['abstract_inverted_index'] = pyalexInfo['abstract_inverted_index']
                pass

        save_generic(self.papers_set_path, self.papers_set)
        save_generic(self.references_list_path, self.references_list)

    def split_info_to_serve(self, doi, schInfo, crossInfo, pyalexInfo):
        tempSch = schInfo
        data = {}

        if 'found' in schInfo:
            data = tempSch
            # del Data['references']
        else:
            data = crossInfo
            # del Data['reference']

        if 'author' in crossInfo:
            data['authorsCross'] = crossInfo['author']
        if 'authorships' in pyalexInfo:
            data['authorsPyAlex'] = pyalexInfo['authorships']
        if 'abstract_inverted_index' in pyalexInfo:
            abstract = self.reconstruir_abstract(
                doi, pyalexInfo, pyalexInfo['abstract_inverted_index'])
            data['abstract'] = abstract
            # Data['abstract_inverted_index'] = pyalexInfo['abstract_inverted_index']

        data = pyalexInfo | schInfo

        #self.check_references(doi, schInfo, crossInfo, pyalexInfo)
        #Data = self.delete_refs(Data)
        self.papers_set[doi] = data
        # print('fin')

    def reconstruir_abstract(self, doi, api_info, abstract_inverted_index):
        try:
            # Ordenar el diccionario por los valores de las posiciones
            sorted_index = sorted(
                abstract_inverted_index.items(), key=lambda x: x[1][0])
            # Reconstruir el abstract
            abstract = ' '.join([key for key, _ in sorted_index])
            return abstract
        except Exception as e:
            print(f'Supuesto abstract {api_info}')
            info = search_papers_sch(doi)
            # info2 = search_in_crossref(doi)
            if 'abstract' in info:
                if info['abstract'] is not None:
                    return info['abstract']
            print(e)
            return ''

    def delete_refs(self, data):
        if 'references' in data:
            del data['references']
        if 'reference' in data:
            del data['reference']
        if 'authorships' in data:
            del data['authorships']
        return data

    def check_references(self, doi, schInfo, crossInfo, pyalexInfo):
        try:

            if schInfo['found']:
                if len(schInfo['references']) > 0:
                    dataref = {
                        'dataType': 'sch',
                        'references': schInfo['references']
                    }
                    self.references_list[doi] = dataref

                elif len(crossInfo['reference']) > 0:
                    dataref = {
                        'dataType': 'cross',
                        'references': crossInfo['reference']
                    }
                    self.references_list[doi] = dataref

            elif crossInfo['found']:
                if len(crossInfo['reference']) > 0:
                    dataref = {
                        'dataType': 'cross',
                        'references': crossInfo['reference']
                    }
                    self.references_list[doi] = dataref

        except Exception as e:
            fail_message(e)
            print(f"IN references : Paper with ID {doi} not found. {e}")

        # print('fin')

    def check_authors(self, path):
        authors = load_generic(path)
        namesOfAuthors = {}
        path_to_save = 'Data/names_by_authors.json'

        for key, value in authors.items():
            name = value['name']
            if name not in namesOfAuthors:
                data = {
                    'is_duplicated': False,
                    'list': [key]
                }
                namesOfAuthors[name] = data
            else:
                print(f'Autor duplicado {name}')
                namesOfAuthors[name]['list'].append(key)
                namesOfAuthors[name]['is_duplicated'] = True

        save_generic(path_to_save, namesOfAuthors)

    def merge_duplicated_authors(self, authorsPath, institutionsPath):
        path = 'Data/names_by_authors.json'
        nameAuthors = load_generic(path)
        authors = load_generic(authorsPath)
        institutions = load_generic(institutionsPath)
        for key, value in nameAuthors.items():
            if value['is_duplicated']:
                #duplicado
                authors_list = value['list']
                unique_affiliations = {}
                first_author_id = authors_list[0]
                for i, author_id in enumerate(authors_list):
                    author = authors[author_id]
                    #unique_affiliations.update(aff for aff in author['affiliations'])
                    # Mantener el orden de las afiliaciones y eliminar duplicados
                    for aff in author['affiliations']:
                        if aff['id'] not in unique_affiliations:
                            unique_affiliations[aff['id']] = aff
                    # Modificar la información 'is_duplicated' para los secundarios
                    if i != 0:
                        authors[author_id]['is_duplicated'] = True
                        authors[author_id]['source'] = first_author_id

                #newlist = [ institutions[aff_id] for aff_id in unique_affiliations]
                newlist = list(unique_affiliations.values())
                authors[first_author_id]['affiliations'] = newlist

        newAuthors = 'Data/authors.json'
        save_generic(newAuthors, authors)

    def change_papersmin_authors_duplicated(self, papersminPath):
        papersmin = load_generic(papersminPath)
        authors_dict = load_generic('Data/authors.json')
        for key, value in papersmin.items():
            authors = value['authors']
            for author in authors:
                id = author['id']
                if 'is_duplicated' in authors_dict[id]:
                    author['id'] = authors_dict[id]['source']

        newpapersminpath = 'Data/papersmin2.json'
        save_generic(newpapersminpath, papersmin)