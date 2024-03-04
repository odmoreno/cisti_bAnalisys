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
    save_generic('Data/papers.json', extractdata.mainPapers)
    extractdata.save_data()

if __name__ == '__main__':
    loop_years_list()
    


