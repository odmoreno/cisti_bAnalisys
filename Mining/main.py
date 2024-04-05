'''
Ejecutable principal para hacer el scrapping, los archivos y automatizar
'''
import os

from common_functions import *

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())


def generate_csv_papers_tmp():
    cols = ['type', 'year', 'title', 'doi', 'conference',
            'authors', 'countries', 'regions', 'affiliations']
    conf_check = load_generic('Mining/Data/conference_check.json')
    type = 'Journal Article'
    conf_name = 'vinci'
    papers_to_save = {}
    for id, conf in conf_check.items():
        year = conf['data_published']
        papers = conf['papers']
        for paper in papers:
            doi = paper['doi']
            data = {
                'type': type,
                'year': year,
                'title': paper['title'],
                'doi': doi,
                'conference': conf_name,
                'authors': '',
                'countries': '',
                'regions': '',
                'affiliations': ''
            }
            papers_to_save[doi] = data
    csv_generics('Mining/Data/vinci_papers.csv', papers_to_save.values(), cols)


def loop_csv_cisti():
    years = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010]
    conf_check = {}
    for year in years:
        file = '../Data/years/'+ str(year) + '.csv'
        elements = load_csv(file)
        elements = elements[1:]
        papers = []
        for element in elements:
            title = element[0]
            doi = element[13]
            linkdoi = 'https://doi.org/' + doi

            paper_data = {
                'title': title,
                'doi': doi,
                'url': linkdoi
            }
            papers.append(paper_data)

        data = {
            "data_published": year,
            "publisher": "IEEE",
            'papers': papers
        }
        name = 'cisti_' + str(year)
        conf_check[name] = data
        print(name)

    save_generic('Data/conference_check.json', conf_check)
    print(f"fin")


if __name__ == '__main__':
    #find_list_papers_cisti()
    loop_csv_cisti()