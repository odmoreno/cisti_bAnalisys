from common_functions import *

# Obtén la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Cambia el directorio de trabajo al directorio del script
os.chdir(script_dir)

current_directory = os.getcwd()
print("Directorio de trabajo actual:", os.getcwd())


main_path = 'txt/'

def get_papers(path= '../GetData/Data/papers.json'):
    papers = load_generic(path)
    return papers

def loop_papers():
    vacio = 0
    papers = get_papers()
    for id, paper in papers.items():
        abstract = paper['abstract']
        title = paper['title']

        if abstract == '':
            vacio += 1

        full_text = f"""{title}
ABSTRACT
{abstract}
"""
        file_path = main_path + id + '.txt'
        # Guardar el texto en un archivo
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(full_text)
            # print(f"Escrito archivo {file_path}")

    print(f"fin fun {vacio}")

if __name__ == '__main__':

    loop_papers()
