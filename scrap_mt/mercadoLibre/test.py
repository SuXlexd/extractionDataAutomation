"""
    Este script es el encargado de generar los nuevos WebDrivers para scrapear 
    los datos y recolectar los links de mercado libre.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

SERVICE= Service(ChromeDriverManager().install())

def get_new_driver():
    """
    Crea y retorna una nueva instancia del navegador Chrome con opciones predefinidas.

    Returns:
        selenium.webdriver.Chrome: Navegador Chrome con configuración personalizada.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')

    return webdriver.Chrome(service=SERVICE, options=chrome_options)


def getPrecios(driver):
    try:
        precios = driver.find_elements(By.XPATH, '//div[@class="ui-pdp-price__main-container"]//span[@class="andes-money-amount__fraction"]')
        
        if not precios:
            return 0, 0  # Si no se encuentran precios, devolver 0, 0        
        precioVenta=0
        precioOriginal=0

        print(precios)

        def clear(prices,index):
            return float(prices[index].text.replace(',',''))

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
                precioOriginal=precios[0].text
                precioVenta=precios[1].text
            
        elif len(precios) >= 3:
                precioOriginal=precios[0].text
                precioVenta=precios[1].text
        
        
        return precioOriginal, precioVenta
    
    except NoSuchElementException as e:
        print(f'Error al encontrar elementos de precio: {e}')
        return 0, 0


def get_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//span[text()='Siguiente']/ancestor::a")
        next_button.click()
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    driver = get_new_driver()
    links=['https://listado.mercadolibre.com.mx/llantas']
    driver.get(links[0])
    get_next_page(driver);
    sleep(10)
    driver.quit()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
# SERVICE= Service(ChromeDriverManager().install())
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--disable-extensions')
# driver=webdriver.Chrome(service=SERVICE, options=chrome_options)
# driver.get('https://listado.mercadolibre.com.mx/llantas')
# btn=driver.find_element(By.CSS_SELECTOR,"li.andes-pagination__button.andes-pagination__button--next a.andes-pagination__link")
# driver.execute_script("""arguments[0].scrollIntoView({block: 'center', inline: 'center'});""", btn)