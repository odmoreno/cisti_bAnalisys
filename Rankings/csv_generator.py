'''
Generar todos los csv habidos y por haber
'''


from common_functions import *


class CsvGenerator:

    def __init__(self):
        # WorldCist proceedings
        self.conference_url = "https://link.springer.com/conference/worldcist"
        self.datapath = 'ranking/'

    def set_years_list(self, yearsList):
        # Convertir la lista de años a una lista de strings
        self.years_as_strings = [str(year) for year in yearsList]

    def create_csv_rankings(self, sourcePath, destinyPath, _isRegion = False, _isCountry=False):
        data = load_generic(sourcePath)
        cols = ["id", "name", "country", "region"]
        isRegion = False
        isCountry = False
        if _isRegion:
            cols = ["id", "name"]
            isRegion = True
        if _isCountry:
            cols = ["id", "name", "region"]
            isCountry = True

        self.create_csv_per_years(destinyPath, data, cols, _isRegion= isRegion, _isCountry=isCountry)

    def create_csv_per_years(self, path, data, cols, _isRegion = False, _isCountry=False):
        # Abrir el archivo CSV en modo de escritura
        with open(path, "w", newline="", encoding="utf-8") as file:
            # Crear un objeto escritor CSV
            writer = csv.writer(file)
            # Escribir el encabezado del CSV
            writer.writerow(cols + self.years_as_strings + ["total"])
            # Escribir los datos de cada autor y sus años en el CSV
            for author_data in data.values():
                author_id = author_data["id"]
                name = author_data["name"]
                total = author_data["total"]
                years_data = [str(author_data["years"].get(str(year), 0)) for year in self.years_as_strings]
                if _isCountry:
                    region = author_data['region']
                    writer.writerow([author_id, name, region] + years_data + [total])
                elif _isRegion:
                    writer.writerow([author_id, name] + years_data + [total])
                else:
                    # Escribir la fila en el CSV
                    pais = author_data['country']
                    region = author_data['region']
                    writer.writerow([author_id, name, pais, region] + years_data + [total])
            print(f'Fin {path}')


