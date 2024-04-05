'''
Rankings o estadisticas v2
'''

from common_functions import *
from coauthor import PapersData
from rank_options import RankMenu

import os

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())

def create_ranking_data():
    #predata necesaria
    papers_path = '../GetData/Data/papersUpdate.json'
    author_path = '../GetData/Data/authorsU.json'
    name_conf = 'Cisti'
    year_list = [2010,2011,2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    #Instancia de ranking
    rank_menu = RankMenu()
    rank_menu.load_data_for_loop(papers_path, name_conf, year_list)
    #Generamos los jsons para cada conf
    rank_menu.loop_papers_in_conference()
    #ranking csv
    rank_menu.create_csv_rankings()
    #authors.csv
    rank_menu.create_csv_authors(path=author_path)
    #papers_worldcist.csv
    rank_menu.generate_csv(papers_path)

def create_coauthors():
    client = PapersData()
    conf = load_generic('../GetData/Data/papersUpdate.json') #'../Papers/Data/papersmin4.json'
    client.loop_conferences('Cisti', conf)


if __name__ == '__main__':
    create_ranking_data()
    create_coauthors()

    print(f'FIN de main Ranking 2')