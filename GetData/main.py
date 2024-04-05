'''
Obtener los autores, instituciones,  paises

doi si es que tiene
abstract
y link de descarga de pdf

1. leer los csv en orden 
2. extraer one by one la informacion

'''

from common_functions import *
from extract_data import ExtractData

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())


years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

def loop_years_list():
    mainpath = '../Data/years/'

    extractdata = ExtractData()

    for element in years:
        filename = mainpath + element + '.csv'
        papers_in_this_year, min_papers = extractdata.leer_csv_y_crear_objetos_dict(filename, element)
        print('fin')
        filejson = 'Data/full/' + element + '.json'
        filejson2 = 'Data/min/' + element + '.json'
        # Guardar el diccionario en el archivo JSON
        save_generic(filejson, papers_in_this_year)
        save_generic(filejson2, min_papers)

    print('imprimir todos los datos')
    extractdata.save_data()
    save_generic('Data/papers.json', extractdata.mainPapers)
    save_generic('Data/papersmin.json', extractdata.mainPapersmin)


def check_affs_map():
    '''
        1. revisar las afiliaciones en papersmin.json
        2. revisar las afiliaciones en authors.json
        3. revisar las afiliaciones en affiliations2.json
        4. reemplazar con los valores de affmap.json
    '''

    loop_papersmin()
    loop_authors()


def loop_papersmin():

    papersmin = load_generic('Data/papersmin.json')
    for idpaper, paper in papersmin.items():
        authors = paper['authors']
        for author in authors:
            aff = author['affiliations']
            value = validate_aff(aff)
            if value:
                aff['name'] = value['name']
                aff['code'] = value['code']
                aff['id'] = value['code']
                aff['country'] = value['country']
                aff['region'] = value['region']

    save_generic('Data/papersUpdate.json', papersmin)


def loop_authors():
    authorsDict = load_generic('Data/authors.json')
    for idau, data in authorsDict.items():
        affs = data['affiliations']
        for aff in affs:
            value = validate_aff(aff)
            if value:
                aff['name'] = value['name']
                aff['code'] = value['code']
                aff['id'] = value['code']
                aff['country'] = value['country']
                aff['region'] = value['region']

    save_generic('Data/authorsU.json', authorsDict)


def loop_affiliations():
    affiliationsDict = load_generic('Data/affiliations2.json')
    for id, data in affiliationsDict.items():
        pass


def validate_aff(aff):
    # value = {}
    code = aff['code']
    affiliations = load_generic('../Data/affiliations.json')
    affmap = load_generic('Data/affmap.json')
    for key, value in affmap.items():
        if key in code:
            # value = affmap[key]
            affback = affiliations[value]
            return affback


if __name__ == '__main__':
    # loop_years_list()
    check_affs_map()
    


