import os
import shutil
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common_functions import *


carpeta_destino = 'Data/'
# cargar elementos
papers = load_generic('../GetData/Data/papersmin.json')

# Obtener la ruta absoluta de la carpeta del proyecto
ruta_proyecto = os.path.abspath(os.path.dirname(__file__))
# Definir la subcarpeta donde deseas que se guarden las descargas
subcarpeta_descargas = 'Data'
# Combinar la ruta del proyecto con la subcarpeta de descargas
ruta_descargas = os.path.join(ruta_proyecto, subcarpeta_descargas)

def generar_pdfs():
    driver = init_driver()
    for id, paper in papers.items():
        pdflink = paper.get('pdflink')
        if pdflink:
            nombre_archivo = paper.get('id') + '.pdf'
            # Ruta completa del archivo en la carpeta destino
            ruta_archivo = os.path.join(subcarpeta_descargas, nombre_archivo)
            # Verificar si el archivo ya existe en la carpeta destino
            #if not os.path.exists(ruta_archivo):
            if True:
                try:
                    #https://learning-analytics.info/index.php/JLA/article/view/8409/7781
                    #driver.get(pdflink)
                    driver.get("https://learning-analytics.info/index.php/JLA/article/view/8409/7781")

                    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
                    loop_iframes(iframes, driver)
                    change_name(nombre_archivo)
                    print(f"Cambiado  a {nombre_archivo}")
                except Exception as e:
                    print(f"Error {e} al cambiar de nombre: {pdflink} ")

            else:
                pass
                #print(f"El archivo {nombre_archivo} ya existe en la carpeta 'pdfs'. No se descargará nuevamente.")

    print("fin")

def test(url='https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&amp;arnumber=10211664&amp;ref='):
    respuesta = requests.get(url)
    status = respuesta.status_code
    print(status)

def init_driver():
    profile = {
        'download.prompt_for_download': False,
        'download.default_directory': ruta_descargas,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True,
        'download.default_filename': 'test'
    }
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', profile)
    driver = webdriver.Chrome(options=options)
    return driver

def loop_iframes(iframes, driver):
    for iframe in iframes:
        src = iframe.get_attribute('src')
        if src:
            print("Encontrado iframe con src:", src)
            try:
                # Cambiar al contexto del iframe
                driver.switch_to.frame(iframe)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body')))
                driver.find_element(By.TAG_NAME, 'button').click()
                # Cambiar de nuevo al contexto predeterminado
                driver.switch_to.default_content()
                # Esperar un tiempo suficiente para que se complete la descarga
                time.sleep(60)  # Ajusta el tiempo según sea necesario
                return
            except Exception as e:
                print("Error al hacer clic en el iframe:", e)

def change_name(pdfname):
    # Obtener la lista de archivos en la carpeta de descargas
    archivos = os.listdir(ruta_descargas)
    # Filtrar solo los archivos, excluyendo los directorios
    archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(ruta_descargas, archivo))]
    # Ordenar los archivos por fecha de modificación (el más reciente al final)
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(ruta_descargas, x)))
    # Obtener el último archivo de la lista (el más reciente)
    ultimo_archivo = archivos[-1]
    ruta_ultimo = os.path.join(ruta_descargas, ultimo_archivo)
    nuevo_nombre = os.path.join(ruta_descargas, pdfname)
    renombrar_archivo(ruta_ultimo, nuevo_nombre)

# Función para renombrar el archivo descargado
def renombrar_archivo(nombre_actual, nuevo_nombre):
    os.rename(nombre_actual, nuevo_nombre)

if __name__ == '__main__':
    generar_pdfs()