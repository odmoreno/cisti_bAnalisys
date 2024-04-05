import os
import shutil
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Función para renombrar el archivo descargado
def renombrar_archivo(nombre_actual, nuevo_nombre):
    os.rename(nombre_actual, nuevo_nombre)


'''
<iframe src="https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&amp;arnumber=10211664&amp;ref=" frameborder="0"></iframe>
		
<iframe sandbox="allow-scripts allow-same-origin" title="Adobe ID Syncing iFrame" id="destination_publishing_iframe_ieeexplore_0" 
name="destination_publishing_iframe_ieeexplore_0_name" 
src="https://ieeexplore.demdex.net/dest5.html?d_nsid=0#https%3A%2F%2Fieeexplore.ieee.org" class="aamIframeLoaded" style="display: none; width: 0px; height: 0px;"></iframe><div class="pub_300x250 pub_300x250m pub_728x90 text-ad textAd text_ad text_ads text-ads text-ad-links" style="width: 1px !important; height: 1px !important; position: absolute !important; left: -10000px !important; top: -1000px !important;"></div></body></html>

<a href="https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&amp;arnumber=10211664&amp;ref=" target="_blank">
          <button id="open-button" tabindex="1">Open</button>
        </a>
        
'''

'''
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": "/Users/CTI/Downloads",
    "download.prompt_for_download": False,  # Desactiva el diálogo de confirmación de descarga
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
'''

# Obtener la ruta absoluta de la carpeta del proyecto
ruta_proyecto = os.path.abspath(os.path.dirname(__file__))

# Definir la subcarpeta donde deseas que se guarden las descargas
subcarpeta_descargas = 'Data'

# Combinar la ruta del proyecto con la subcarpeta de descargas
ruta_descargas = os.path.join(ruta_proyecto, subcarpeta_descargas)

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

# Inicializa el navegador con las opciones configuradas
driver = webdriver.Chrome(options=options)

# URL de la página que contiene el enlace al PDF
url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10211664'

# Accede a la página
driver.get(url)

# Obtén el contenido de la página
contenido = driver.page_source

# Imprime el contenido (o realiza cualquier otra operación que desees)
print(contenido)

testurl = 'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&amp;arnumber=10211664&amp;ref='

iframes = driver.find_elements(By.TAG_NAME, 'iframe')

# Iterar sobre los iframes y hacer clic en cada uno
for iframe in iframes:
    src = iframe.get_attribute('src')
    if src:
        print("Encontrado iframe con src:", src)
        try:
            # Cambiar al contexto del iframe
            driver.switch_to.frame(iframe)
            # Esperar a que el iframe sea interactivo
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body')))
            # Realizar clic en algún elemento del iframe (por ejemplo, el body)
            driver.find_element(By.TAG_NAME, 'button').click()
            # Realizar las acciones necesarias dentro del iframe
            # Puedes agregar aquí cualquier otra acción que necesites realizar dentro del iframe
            # Cambiar de nuevo al contexto predeterminado
            driver.switch_to.default_content()
            # Esperar un tiempo suficiente para que se complete la descarga
            time.sleep(30)  # Ajusta el tiempo según sea necesario

            # Obtener la lista de archivos en la carpeta de descargas
            archivos = os.listdir(ruta_descargas)
            # Filtrar solo los archivos, excluyendo los directorios
            archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(ruta_descargas, archivo))]
            # Ordenar los archivos por fecha de modificación (el más reciente al final)
            archivos.sort(key=lambda x: os.path.getmtime(os.path.join(ruta_descargas, x)))
            # Obtener el último archivo de la lista (el más reciente)
            ultimo_archivo = archivos[-1]
            ruta_ultimo = os.path.join(ruta_descargas, ultimo_archivo)
            nuevo_nombre = os.path.join(ruta_descargas, 'test2.pdf')
            renombrar_archivo(ruta_ultimo, nuevo_nombre)


        except Exception as e:
            print("Error al hacer clic en el iframe:", e)



# Localiza el enlace al PDF y haz clic en él para iniciar la descarga
enlace_pdf = driver.find_element( By.XPATH, '//a[@target="_blank"]')

driver.find_element_by_class_name('href-button')

#enlace_pdf = driver.find_element_by_xpath('//a[@target="_blank"]')
enlace_pdf.click()



# Cierra el navegador
driver.quit()


