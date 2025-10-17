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
location_id = 2
date_format = '%Y-%m-%d %H:%M:%S'
sql_registers_max_x_query = 10
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
sql_db = 'aasydcom_espot_scraping_tires_moto_mx'
# sql_db = 'aasydcom_espot_scraping_tires_tester_mx'

# Sitio: item cargado para sitio listo
ITEM_READY = '/html/body/main/div/div[2]/section'
ITEM_READY_PAG = '/html/body'

# Sitio: item por tire
tag_tire = 'ui-search-layout__item'
tag_item = 'tbody'
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
LINK_WEB = 'https://www.motocity.mx/listado/accesorios-vehiculos/llantas/llantas-motos/'
# LINK_WEB = 'https://www.motocity.mx/listado/accesorios-vehiculos/llantas/llantas-motos/_Desde_151_NoIndex_True'
# LINK_WEB = 'https://www.motocity.mx/listado/accesorios-vehiculos/llantas/llantas-motos/_Desde_201_NoIndex_True'


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
    text = text.strip().replace("$", "").replace(",", "")
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
elements_root = []
elements_brands = []
elements_tires = []
reading_content = True
while reading_content:

    # Seleccionar, cargar sitio y espera inicial
    driver.get(link_web_id)
    sleep(random_time(TIME_RANGE_SM))

    # Esperando elemento cargado para notificar de sitio listo
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, ITEM_READY)))

    # Descender al final del sitio para cargar todos los elementos
    i = 0
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(random_time(TIME_RANGE_MD))
        if check_exists_by_class(driver.find_element(By.XPATH, "/html/body"), 'andes-pagination') or i == 10:
            break
        else:
            i += 1
            print('PAGINA : ' + str(i))

    tires = driver.find_elements(By.CLASS_NAME, tag_tire)
    for tires_iterator in range(len(tires)):
        # elements_brands.append('"' + tires[tires_iterator].find_elements(By.TAG_NAME, 'img')[1].get_attribute('title').upper() + '"')
        # elements_tires.append('"' + tires[tires_iterator].find_elements(By.TAG_NAME, 'img')[0].get_attribute('title').upper() + '"')
        elements_url.append(tires[tires_iterator].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))
        elements_root.append(link_web_id)

    # Secuencia para detectar ultima pagina de categoria del sitio
    print(link_web_id)

    # Espera por pagina
    sleep(random_time(TIME_RANGE_MD))

    if len(driver.find_elements(By.CLASS_NAME, 'andes-pagination__button--next')):
        link_web_id = driver.find_elements(By.CLASS_NAME, 'andes-pagination__button--next')[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
    else:
        reading_content = False


# Inicializar variables por categoria del sitio
parciales = []
now = datetime.datetime.now()
timestamp_now = '"' + now.strftime(date_format) + '"'

for url_iterator in range(len(elements_url)):


    # Seleccionar, cargar sitio y espera inicial
    driver.get(elements_url[url_iterator])
    sleep(random_time(TIME_RANGE_SM))

    # Esperando elemento cargado para notificar de sitio listo
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, ITEM_READY_PAG)))

    # Descender al final del sitio para cargar todos los elementos
    i = 0
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(random_time(TIME_RANGE_MD))

        if check_exists_by_class(driver.find_element(By.XPATH, "/html/body"), 'footer') or i == 10:
            break
        else:
            i += 1
            print('PAGINA : ' + str(i))

    if i == 10:
        break

    tablas = driver.find_elements(By.TAG_NAME, tag_item)
    print('CATEGORIZANDO...')
    data_name = value_null
    data_brand = value_null
    data_line = value_null
    data_code = value_null
    data_count = value_null
    data_origin = value_null
    data_terrain = value_null
    data_ad = value_null
    data_category = value_null
    data_position = value_null
    data_index = value_null
    data_speed_rating = value_null
    data_TL = value_null
    data_width = value_null
    data_ratio = value_null
    data_rim = value_null
    data_type = value_null
    for tabla in range(len(tablas)):
        elementos = tablas[tabla].find_elements(By.TAG_NAME, 'tr')
        for elemento in range(len(elementos)):
            parametro = prepare_string_to_db(elementos[elemento].find_elements(By.TAG_NAME, 'th')[0].get_attribute("innerHTML"))
            valor = elementos[elemento].find_elements(By.TAG_NAME, 'td')[0].find_elements(By.TAG_NAME, 'span')[0].get_attribute("innerHTML")
            if parametro == "Modelo":
                data_name = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Marca":
                data_brand = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Línea":
                data_line = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Tamaño":
                data_code = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Cantidad de llantas":
                data_count = float(re.findall('[\d.]+', prepare_string_to_db(valor))[0])
            elif parametro == "Origen":
                data_origin = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Tipo de terreno":
                data_terrain = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Tipo de adherencia":
                data_ad = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Estilo":
                data_category = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Posición":
                data_position = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Índice de velocidad":
                data_speed_rating = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Índice de carga":
                if re.match('[\d.]+', prepare_string_to_db(valor)) is not None:
                    data_index = re.findall('[\d.]+', prepare_string_to_db(valor))[0]
                # try:
                #     data_speed_rating = '"' + re.findall("[A-Z]+", prepare_string_to_db(valor).upper())[0] + '"'
                # except:
                #     print(data_code+" NO data_ratio")
            elif parametro == "Tipo de montaje":
                data_TL = '"' + prepare_string_to_db(valor).upper() + '"'
            elif parametro == "Ancho de sección":
                data_width = re.findall('[\d.]+', prepare_string_to_db(valor))[0]
            elif parametro == "Relación de aspecto":
                data_ratio = re.findall('[\d.]+', prepare_string_to_db(valor))[0]
            elif parametro == "Diámetro del rin":
                data_rim = re.findall('[\d.]+', prepare_string_to_db(valor))[0]
            elif parametro == "Tipo de moto":
                data_type = '"' + prepare_string_to_db(valor).upper() + '"'
    # if data_code == value_null:
    #     break
    # if data_name == value_null:
    #     break
    # info producto
    data_price_con_iva = float(prepare_string_to_price(prepare_string_to_db(driver.find_elements(By.CLASS_NAME, 'andes-money-amount__fraction')[0].text)))
    if data_count != 1 and data_count != value_null:
        data_price_con_iva = data_price_con_iva / data_count
    data_price_sin_iva = data_price_con_iva / factor_tax;
    data_original_con_iva = data_price_con_iva
    data_original_sin_iva = data_price_sin_iva
    data_price_con_iva_usd = data_price_con_iva / rate_exchange
    data_price_sin_iva_usd = data_price_sin_iva / rate_exchange

    # String query x element
    string_query = prepare_string_to_query(location_id, data_name, data_brand,
                                             data_code,
                                             data_width, data_ratio, data_rim,
                                             data_original_sin_iva, data_original_con_iva,
                                             data_price_sin_iva, data_price_con_iva,
                                             data_price_sin_iva_usd, data_price_con_iva_usd,
                                             rate_exchange, rate_tax,
                                             data_index, data_speed_rating,
                                             data_category,
                                             '"' + elements_url[url_iterator] + '"', 0,
                                             timestamp_now)
    parciales.append(string_query)
    print(string_query)
    print('\n')

    if len(parciales) >= sql_registers_max_x_query:
        database = DataBase()
        database.parciales = parciales
        database.insert_register()
        parciales = []


# Espera para cargar base y cerrar navegador
sleep(random_time(TIME_RANGE_LG))
driver.close()
