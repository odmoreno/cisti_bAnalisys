'''
Ejecutable principal para sacar la info de los papers en las conferencias
'''
import os

from common_functions import *
from papers_info import PapersInfo
from update_info_in_papers import UpdateData

root = 'Data/'

def loop_proocedings(_flag=False, conference_path='../Mining/Data/conference_check.json', paper_path='Papers/Data/papers.json', ref_path='Papers/Data/ref_list.json'):
    if _flag:
        papersInfo = PapersInfo()
        # establecemos la ruta de los papers
        papersInfo.papers_set_path = paper_path
        # papers ref path
        papersInfo.references_list_path = ref_path
        # establecemos la ruta de las conferencias
        papersInfo.proceeding_path = conference_path
        papersInfo.proocedings_list = load_generic(papersInfo.proceeding_path)
        # recorremos las conferencias y generamos los archivos papers.json
        papersInfo.loop_proocedings(papersInfo.proocedings_list)


def create_jsons_from_paper_data(_flag=False):
    if _flag:
        papers_info = UpdateData()
        paper_path = root + 'papers.json'
        paperminpath = root + 'papersmin.json'
        affiliations_path = root + 'institutions.json'
        auth_path = root + 'authors_info.json'
        papers_info.set_paramethers(
            paper_path, paperminpath, affiliations_path, auth_path)
        papers_info.check_papers()


def clear_duplicated_authors():
    papersInfo = PapersInfo()
    authors_path = 'Data/authors_info.json'
    institutions_path = 'Data/institutions.json'
    papersminpath = 'Data/papersmin.json'
    papersInfo.check_authors(authors_path)
    papersInfo.merge_duplicated_authors(authors_path, institutions_path)
    papersInfo.change_papersmin_authors_duplicated(papersminpath)


if __name__ == '__main__':

    loop_proocedings(False, conference_path='../Mining/Data/conference_check.json',
                     paper_path='Data/papers.json', ref_path='Data/ref_list.json')

    create_jsons_from_paper_data(_flag=True)

    #clear_duplicated_authors()


