from src.utils.wait import wait_scrap, wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.procedures.prints import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from datetime import datetime
from selenium import webdriver
from .driver_factory import get_new_driver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from PIL import Image
import os

import sys

from time import sleep

def extr(e):
    return e.accessible_name

def isPaused(driver):
    try:
        e=driver.find_element(By.XPATH, '//div[contains(.,"Publicación pausada")]')
        return True
    except Exception as e:
        return False
    
def isInexistent(driver):
    try:
        e = driver.find_element_by_xpath('//h4[@class="ui-empty-state__title" and text()="Parece que esta página no existe"]')
        return True
    except Exception as e:
        return False

def getStore(driver):
    try:
        return driver.find_element(By.XPATH, '//div[@class="ui-pdp-seller__header__title"]//span[@class=""]').text
    except Exception as e:
        return ""

def getStock(driver):
    try:
        disponibles = int(driver.find_element(By.CSS_SELECTOR, '.ui-pdp-buybox__quantity__available').text.replace('(','').replace(' disponibles)',''))
        return disponibles
    except Exception as e:
        return 0

def fuimosTimados(driver):
    try:
        h4 = driver.find_element(By.XPATH, '//h4[@class="ui-empty-state__title"]')
        if 'Tenemos un problema' in h4.text:
            return True
    except Exception as e:
        return False
    return False


# def getPrecios(driver):
#     try:
#         precios = driver.find_elements(By.XPATH, '//div[@class="ui-pdp-price__main-container"]//span[@class="andes-money-amount__fraction"]')
        
#         if not precios:
#             return 0, 0  # Si no se encuentran precios, devolver 0, 0        
#         precioVenta=0
#         precioOriginal=0

#         if len(precios) == 1:
#             precioVenta=precios[0].text
#             precioOriginal=precios[0].text
        
#         elif len(precios) == 2:
#             '''
#                 Este es el caso interesante, se debe deducir cual es el caso_
#                 CASO 1: precio venta                5,600
#                         fraccion de precio MSI      12 meses de 466
                    
#                 CASO 2: precio original:            4,000
#                         precio venta:               3,900

#             '''
#             case=0
#             try:
#                 #Recuperamos el contenedor de los precios
#                 prices_container=driver.find_element(By.XPATH, '//div[@class="ui-pdp-price__main-container"]')
#                 #Revisamos si tiene el contenedor de meses sin intereses:
#                 there_is=prices_container.find_element(By.XPATH, './/p[@class="ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--REGULAR"]')
#                 #Si no falla existe, por lo tanto se trata del primer caso
#                 case=1
#             except:
#                 #Si falla, no existe, por lo tanto se trata del segundo caso
#                 case=2

#             if(case==1):
#                 precioOriginal=precios[0].text
#                 precioVenta=precios[0].text
#             if(case==2):
#                 precioOriginal=precios[0].text
#                 precioVenta=precios[1].text
            
#         elif len(precios) >= 3:
#                 precioOriginal=precios[0].text
#                 precioVenta=precios[1].text
        
        
#         return precioOriginal, precioVenta
    
#     except NoSuchElementException as e:
#         print(f'Error al encontrar elementos de precio: {e}')
#         return 0, 0
def getPrecios(driver):
    try:
        precios = driver.find_elements(By.XPATH, '//div[@class="ui-pdp-price__main-container"] //span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"] //span[@class="andes-money-amount__fraction"]')
        if not precios:
            return 0, 0  # Si no se encuentran precios, devolver 0, 0        
        precioVenta=0
        precioOriginal=0
        if len(precios) == 1:
            precioVenta=precios[0].text
            precioOriginal=precios[0].text
        elif len(precios) == 2:
            '''
                Este es el caso interesante, se debe deducir cual es el caso_
                CASO 1: precio venta                5,600
                        fraccion de precio MSI      12 meses de 466
                   
                CASO 2: precio original:            4,000
                        precio venta:               3,900
 
            '''
            case=0
            try:
                #Recuperamos el contenedor de los precios
                prices_container=driver.find_element(By.XPATH, '//div[@class="ui-pdp-price__main-container"]')
                #Revisamos si tiene el contenedor de meses sin intereses:
                there_is=prices_container.find_element(By.XPATH, './/p[@class="ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--REGULAR"]')
                #Si no falla existe, por lo tanto se trata del primer caso
                case=1
            except:
                #Si falla, no existe, por lo tanto se trata del segundo caso
                case=2
            if(case==1):
                precioOriginal=precios[0].text
                precioVenta=precios[0].text
            if(case==2):                                       
                precioOriginal=driver.find_element(By.XPATH, "/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span/span[2]").get_attribute('innerHTML')
                precioVenta=driver.find_element(By.XPATH, "/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span/span[2]").get_attribute('innerHTML')
        elif len(precios) >= 3:
                precioOriginal=precios[0].text
                precioVenta=precios[0].text
                
        print(f'\n Precios obtenidos: {precioOriginal}, {precioVenta} \n \n')
        print("----------------------------------------")
        return precioOriginal, precioVenta
    except NoSuchElementException as e:
         print(f'Error al encontrar elementos de precio: {e}')
         return 0, 0

def until_complete(link,driver, retries=5, wait_time=6):
    # Reintenta la operación hasta 'retries' veces
    for i in range(retries):
        try:
            driver.get(link)
            #Verifica si 
            if fuimosTimados(driver):
                wait(3600,'dots',"Detectados!!!! 1 hora de espera", bar=True, percentage=False, seconds=True, clear=True)
                return False
            # Verifica si la página está en pausa o necesita interacción
            if isPaused(driver):
                wait(wait_time,'dots',"Publicacion pausada, esperando para siguiente pagina...", bar=True, percentage=False, seconds=True, clear=True)
                return False  # Termina la función sin devolver un driver
            
            #Verificar si el link ya no existe
            if isInexistent(driver):
                wait(wait_time,'dots',"Link expirado, esperando para siguiente pagina...", bar=True, percentage=False, seconds=True, clear=True)
                return False
            
            #Links que deberia rechazar
            refused_links=['https://listado.mercadolibre.com.mx/accesorios-vehiculos/llantas/llantas-autos-camionetas/#redirectedFromVip']   
            if driver.current_url in refused_links:
                wait(wait_time,'dots',"Link en lista negra, esperando para siguiente pagina...", bar=True, percentage=False, seconds=True, clear=True)
                return False
            try:
                # Usa una espera explícita para verificar la presencia de un elemento específico
                WebDriverWait(driver, 4).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//th[@class="andes-table__header andes-table__header--left ui-vpp-striped-specs__row__column ui-vpp-striped-specs__row__column--id"]'))
                )
                return True  # Devuelve el driver si se encuentran los elementos
            except (NoSuchElementException, TimeoutException):
                # Si el elemento no se encuentra o hay una excepción de tiempo, espera y refresca la página
                wait_scrap(wait_time, 'Esperando por información incompleta...')
                driver.refresh()  # Refresca la página para intentar nuevamente
        except WebDriverException as e:
            # Muestra un mensaje de error si ocurre alguna excepción de WebDriver
            print(colored(f'\tError en link: {e}', 'red'))
    # Si el ciclo termina sin éxito, devuelve None indicando que no se pudo completar
    return False


SERVICIO = Service(ChromeDriverManager().install(), log_path=os.devnull)



def screenshot(link, name):
    if name == 'modelo-medida':
        return 'error'

    name = name.replace(" ", "-").replace("/", "-")

    try:
        # Configuración del navegador
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1600,1000")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")  
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(service=SERVICIO, options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        driver.get(link)
        
    except Exception as e:
        return 'no_ss'

    try:
        driver.find_element(By.XPATH, '//span[contains(normalize-space(.),"Más tarde")]').click()
    except:
        pass

    today = datetime.today().isoformat(timespec="milliseconds").replace(".", "").replace(":", "")
    current_year = datetime.now().year
    current_month = datetime.now().month

    os.makedirs(f'screenshots/{current_year}/{current_month}', exist_ok=True)

    # Captura inicial en PNG
    temp_path = f'screenshots/{current_year}/{current_month}/{name}_{today}.png'
    driver.save_screenshot(temp_path)
    driver.quit()

    # Convertir a JPEG con calidad reducida (por ejemplo 60%)
    final_path = temp_path.replace('.png', '.jpg')
    with Image.open(temp_path) as img:
        rgb_img = img.convert('RGB')  # JPEG no soporta transparencia
        rgb_img.save(final_path, "JPEG", quality=60, optimize=True)

    # Opcional: eliminar el PNG original para ahorrar espacio
    os.remove(temp_path)

    sys.stdout.flush()
    return final_path


if __name__ == "__main__":
    driver=get_new_driver()
    
    #Dos precios:
    link='https://www.mercadolibre.com.mx/llanta-michelin-22545r17-primacy-4-94w/p/MLM19732800?pdp_filters=price%3A3000-3999#polycard_client=search-nordic&searchVariation=MLM19732800&wid=MLM2248828437&position=4&search_layout=stack&type=product&tracking_id=e744e65c-3e14-4cd8-9f9c-057dcc8d5928&sid=search'
    
    #Un precio:
    link=''
    driver.get(link)
    print(fuimosTimados(driver))
    
    sleep(30)
    