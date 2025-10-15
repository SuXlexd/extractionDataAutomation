# Librerias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re
import random
import pymysql
import datetime

# EXCHANGE MXN TO USD
rate_exchange = 19.4504
rate_tax = 16
factor_tax = rate_tax / 100 + 1
value_null = 'NULL'

# Configuraciones de base
location_id = 5
date_format = '%Y-%m-%d %H:%M:%S'
sql_registers_max_x_query = 50
sql_header = 'INSERT INTO `registers` (`location_id`, `tire`, `brand`,' \
             ' `size`, `size_width`, `size_ratio`, `size_rim`, ' \
             ' `price_og_fr`, `price_og_tx`,' \
             ' `price_mn_fr`, `price_mn_tx`,' \
             ' `price_us_fr`, `price_us_tx`,' \
             ' `rate_exchange`, `rate_tax`,' \
             ' `load_index`, `speed_rating`, ' \
             ' `category`,' \
             ' `scrap_link`, `scrap_index`,' \
             ' `created_at`, `updated_at`) VALUES '
sql_host = 'localhost'
sql_user = 'root'
sql_password = ''
# sql_db = 'tester_scraping_tires_consumo_mx'
sql_db = 'aasydcom_espot_scraping_tires_moto_mx'

# Sitio: item cargado para sitio listo
ITEM_READY = '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[5]/table/tr/td[1]/div/select'

# Sitio: item por tire
tag_tire = '//div[contains(@class,"product-card__name")]'
tag_item = '//div[contains(@class,"available-row")]'
tag_category = 'available-type-variant'
tag_price = 'available-price'
tag_details = 'available-col__size'

# Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Constante rangos de periodos aleatorios
TIME_RANGE_SM = [0, 0.5]
TIME_RANGE_MD = [0.5, 1]
TIME_RANGE_LG = [1, 2]


# Configuraciones de sitio
# Sitio: link
LINK_WEB = 'https://motometa.com.mx/product/categorie/moto/parts/llantas'


class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host=sql_host,
            user=sql_user,
            password=sql_password,
            db=sql_db
        )

        self.cursor = self.connection.cursor()
        self.parciales = None

        print("Conexión establecido exitosamente!")

    def insert_register(self):
        print("Preparando duplas :")
        duplas = self.parciales
        print(duplas)

        consulta = [sql_header]
        consultas = []
        for iterator_dupla in range(len(duplas)):
            consulta.append(duplas[iterator_dupla])
            if (iterator_dupla + 1) % sql_registers_max_x_query == 0:
                consulta[-1] = consulta[-1][:-1] + ';'
                consultas.append("".join(consulta))
                if iterator_dupla + 1 <= len(duplas):
                    consulta = [sql_header]

        if len(duplas) < sql_registers_max_x_query:
            consulta[-1] = consulta[-1][:-1] + ';'
            consultas.append("".join(consulta))

        print(consultas)
        print("Registrando duplas :")

        for iterator_consulta in range(len(consultas)):
            print(consultas[iterator_consulta])
            try:
                self.cursor.execute(consultas[iterator_consulta])
                self.connection.commit()
            except Exception as e:
                print(e)
                raise


# función para generar periodos aleatorios dentro de un rango
def random_time(time_range):
    return random.uniform(time_range[0], time_range[1])


def check_exists_by_class(parent, css_class_name):
    try:
        parent.find_element(By.CLASS_NAME, css_class_name)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_type(parent, type, css_class_name):
    try:
        parent.find_element(type, css_class_name)
    except NoSuchElementException:
        return False
    return True


def prepare_string_to_price(text):
    text = text.strip().replace("$", "").replace(",", "").replace("jkz", "").replace(" ", "")
    if text == "":
        return None
    else:
        return text


def prepare_string_to_db(text):
    text = text.strip().replace("&NBSP;", " ").replace("<BR>", " ")
    if text == "":
        return None
    else:
        return text


def prepare_string_to_query(sql_location_id, sql_data_name, sql_data_brand,
                            sql_data_code, sql_data_width, sql_data_ratio, sql_data_rim,
                            sql_data_original_sin_iva, sql_data_original_con_iva,
                            sql_data_price_sin_iva, sql_data_price_con_iva,
                            sql_data_price_sin_iva_usd, sql_data_price_con_iva_usd,
                            sql_rate_exchange, sql_rate_tax,
                            sql_load_index, sql_speed_rating,
                            sql_data_category,
                            sql_scrap_link, sql_scrap_index,
                            sql_timestamp_now):
    # String query x element
    sql_append = '(%s, %s, %s,' \
                 ' %s, %s, %s, %s,' \
                 ' %s, %s,' \
                 ' %s, %s,' \
                 ' %s, %s,' \
                 ' %s, %s,' \
                 ' %s, %s,' \
                 ' %s,' \
                 ' %s, %s,' \
                 ' %s, %s),'
    # print(sql_append)
    return sql_append % (sql_location_id, sql_data_name, sql_data_brand,
                         sql_data_code, sql_data_width, sql_data_ratio, sql_data_rim,
                         sql_data_original_sin_iva, sql_data_original_con_iva,
                         sql_data_price_sin_iva, sql_data_price_con_iva,
                         sql_data_price_sin_iva_usd, sql_data_price_con_iva_usd,
                         sql_rate_exchange, sql_rate_tax,
                         sql_load_index, sql_speed_rating,
                         sql_data_category,
                         sql_scrap_link, sql_scrap_index,
                         sql_timestamp_now, sql_timestamp_now)


# Inicializamos el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

link_web_id = LINK_WEB
elements_url = []
# elements_brands = []
# elements_tires = []
reading_content = True

print('CARGANDO PAGINA')

# Seleccionar, cargar sitio y espera inicial
driver.get(link_web_id)

while reading_content:

    sleep(random_time(TIME_RANGE_LG))

    # Esperando elemento cargado para notificar de sitio listo
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, ITEM_READY)))

    # Descender al final del sitio para cargar todos los elementos
    i = 0
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(random_time(TIME_RANGE_LG))
        if i == 3:
                break
        else:
            i += 1
            print('PAGINA : ' + str(i))

    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(random_time(TIME_RANGE_LG))
        if driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[3]/ul/li[2]/button") is not None or i == 10:
                break
        else:
            i += 1
            print('PAGINA : ' + str(i))

    tires = driver.find_elements(By.XPATH, tag_tire)
    for tires_iterator in range(len(tires)):
        elements_url.append(tires[tires_iterator].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))

    # Espera por pagina
    sleep(random_time(TIME_RANGE_LG))
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[3]/ul/li[2]/button")))
        # (By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[3]/ul")))
    next_button = driver.find_elements(By.CLASS_NAME, 'page-link')[-1]
    next_button.click()

    if next_button.get_attribute("disabled") is not None:
        reading_content = False

print('CATEGORIZANDO...')
parciales = []
for url_iterator in range(len(elements_url)):

    # Inicializar variables por categoria del sitio
    now = datetime.datetime.now()
    timestamp_now = '"' + now.strftime(date_format) + '"'

    # Seleccionar, cargar sitio y espera inicial
    print(elements_url[url_iterator])
    driver.get(elements_url[url_iterator])
    sleep(random_time(TIME_RANGE_SM))

    # Esperando elemento cargado para notificar de sitio listo
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header[2]/div/div[3]/div/div/div/div[1]/div/button")))
    # WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/button")))
    # Descender al final del sitio para cargar todos los elementos
    i = 0
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(random_time(TIME_RANGE_MD))

        if check_exists_by_class(driver.find_element(By.XPATH, "/html/body"), 'site__footer') or i == 10:
            break
        else:
            i += 1
            print('PAGINA : ' + str(i))

    details = driver.find_elements(By.CLASS_NAME, "spec__row")

    data_name = value_null
    data_brand = value_null
    data_brand = value_null
    data_code = value_null
    data_rim = value_null
    data_code_array = [value_null, value_null, value_null]
    for detail in range(len(details)):
        if len(details[detail].find_elements(By.CLASS_NAME, "spec__name")):
            spec_name = details[detail].find_elements(By.CLASS_NAME, "spec__name")[0].get_attribute("innerText")
            spec_value = details[detail].find_elements(By.CLASS_NAME, "spec__value")[0].get_attribute("innerText")
            # print(spec_name + " :: " + spec_value)
            if spec_name == "Modelo":
                data_name = spec_value
            elif spec_name == "Fabricante":
                data_brand = spec_value
            elif spec_name == "Diámetro":
                data_rim = spec_value
            elif spec_name == "Nacionalidad":
                data_code = spec_value
    data_string = driver.find_elements(By.TAG_NAME, "h1")[0].text
    # print(data_string)
    data_string = data_string.replace("Llanta para Motocicleta", "")
    data_string = prepare_string_to_db(data_string.replace("data_brand", ""))
    if data_name == value_null:
        data_code = re.findall("[\w./-]+", data_string)[0]
        data_name = data_string.replace(data_brand, "")
        data_name = prepare_string_to_db(data_name.replace(data_code, ""))
    else:
        data_string = data_string.replace(data_name, "")
        data_code = re.findall("[\w./-]+", data_string)[0]
    if data_name is None:
        data_name = data_brand
    # info producto
    data_price_con_iva = float(prepare_string_to_price(prepare_string_to_db(driver.find_elements(By.CLASS_NAME, "product__prices")[0].text)))
    data_price_sin_iva = data_price_con_iva / factor_tax;
    data_original_con_iva = data_price_con_iva
    data_original_sin_iva = data_price_sin_iva
    data_price_con_iva_usd = data_price_con_iva / rate_exchange
    data_price_sin_iva_usd = data_price_sin_iva / rate_exchange

    # String query x element
    parciales.append(prepare_string_to_query(location_id, '"' + data_name + '"', '"' + data_brand + '"',
                                             '"' + data_code + '"',
                                             value_null, value_null, data_rim,
                                             data_original_sin_iva, data_original_con_iva,
                                             data_price_sin_iva, data_price_con_iva,
                                             data_price_sin_iva_usd, data_price_con_iva_usd,
                                             rate_exchange, rate_tax,
                                             value_null, value_null,
                                             value_null,
                                             '"' + elements_url[url_iterator] + '"', 0,
                                             timestamp_now))
    print(parciales[-1])
    print('\n')

if len(parciales):
    database = DataBase()
    database.parciales = parciales
    database.insert_register()

# Espera para cargar base y cerrar navegador
sleep(random_time(TIME_RANGE_LG))
driver.close()
