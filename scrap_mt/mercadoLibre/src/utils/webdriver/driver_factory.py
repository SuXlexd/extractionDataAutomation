"""
    Este script es el encargado de generar los nuevos WebDrivers para scrapear 
    los datos y recolectar los links de mercado libre.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SERVICE = Service(ChromeDriverManager().install())

def get_new_driver():
    """
    Crea y retorna una nueva instancia del navegador Chrome con opciones configuradas
    para evitar ser detectado como bot.
    """
    chrome_options = webdriver.ChromeOptions()
    
    # --- Argumentos comunes de evasión ---
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # --- Opcional: evita modo headless si no lo necesitas ---
    # chrome_options.add_argument('--headless=new')
    
    # --- User-Agent personalizado (realista) ---
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    
    # --- Opcional: usar perfil real con cookies/sesión ---
    # chrome_options.add_argument("user-data-dir=/path/to/your/profile")

    driver = webdriver.Chrome(service=SERVICE, options=chrome_options)

    # --- Evasión JavaScript para eliminar 'navigator.webdriver' ---
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    return driver


if __name__ == "__main__":
    driver = get_new_driver()
    driver.get("https://www.mercadolibre.com.mx/")
    sleep(40)
    driver.quit()
