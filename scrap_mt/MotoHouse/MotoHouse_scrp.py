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
location_id = 4
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
             ' `comment`,' \
             ' `created_at`, `updated_at`) VALUES '
sql_host = 'localhost'
sql_user = 'root'
sql_password = ''
sql_db = 'aasydcom_espot_scraping_tires_moto_mx'
# sql_db = 'aasydcom_espot_scraping_tires_tester_mx'

# Sitio: item cargado para sitio listo
ITEM_READY = '/html/body/div[3]/div[2]/div[2]/div[1]/form'

# Sitio: item por tire
tag_item = 'prod-li'
tag_category = 'available-type-variant'
tag_price = 'woocommerce-Price-amount'
tag_details = 'available-col__size'

# Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Constante rangos de periodos aleatorios
TIME_RANGE_SM = [0, 1]
TIME_RANGE_MD = [2, 3]
TIME_RANGE_LG = [4, 6]

# Configuraciones de sitio
# Sitio: link
LINK_WEB = 'https://motohouse.com.mx/shop/?swoof=1&product_cat=mlm169975%2Cmlm420224'

regex_code = "([\d.]+[/×]\d+.\d+)|([\d.]+\d+-\d+)|(\d+/\d+.[Zz][Rr].\d+)|([\d.]+[/]\d+b-\d+)|([\d.]+[/]\d+ B\d+)"
strings_trash = [
    "Llanta Para Moto ",
    "Llanta P/ Moto ",
    "Llanta Moto ",
    "Llanta Para Motocicleta ",
    "Llanta P/ Motocicleta ",
    "Llanta Para Cuatrimoto ",
    "Llanta Doble Propósito ",
    "Llanta Motocicleta ",
    "Llanta Pa+D66ra Motocicleta ",
    "Llanta Para Scooter ",
    "Llanta P/ Scooter ",
    "Llanta Scooter ",
    "Llanta Off Road Para Moto ",
    "Llanta Off Road Para Motocicleta ",
    "Llanta Doble Propósito Para Moto ",
    "Llanta Para Scooter Cara Blanca ",
    "Para Motocicleta ",
    "Para Moto ",
    "O Motoneta ",
    "Cara Blanca ",
    "Llanta "
]


def replace_strings_trash_to_blank(text):
    for string_iterator in range(len(strings_trash)):
        text = text.replace(strings_trash[string_iterator], "")
    return text


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
                            sql_comment,
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
                 ' %s,' \
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
                         sql_comment,
                         sql_timestamp_now, sql_timestamp_now)


# Inicializamos el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Inicializar variables por categoria del sitio
parciales = []
now = datetime.datetime.now()
timestamp_now = '"' + now.strftime(date_format) + '"'

# Seleccionar, cargar sitio y espera inicial
driver.get(LINK_WEB)
sleep(random_time(TIME_RANGE_SM))

# Esperando elemento cargado para notificar de sitio listo
print('CARGANDO PAGINA')
WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, ITEM_READY)))
sleep(random_time(TIME_RANGE_LG))
#driver.execute_script("document.getElementsByName('ppp')[0].options[2].selected = true")
driver.execute_script("document.getElementsByName('ppp')[0].options[3].selected = true")
driver.execute_script("document.getElementsByName('ppp')[0].onchange()")

print('DESPLEGANDO TODOS LOS ELEMENTOS')
sleep(random_time(TIME_RANGE_LG))
WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, ITEM_READY)))
sleep(random_time(TIME_RANGE_LG))
print('ELEMENTOS DEDSPLEGADOS')

# Descender al final del sitio para cargar todos los elementos
i = 0
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(random_time(TIME_RANGE_MD))

    if check_exists_by_class(driver.find_element(By.XPATH, "/html/body"), 'site-footer') or i == 10:
        break
    else:
        i += 1
        print('PAGINA : ' + str(i))

disenios = driver.find_elements(By.CLASS_NAME, tag_item)

print(len(disenios))

print('CATEGORIZANDO...')
for disenio in range(len(disenios)):
    linea = disenios[disenio].find_elements(By.TAG_NAME, 'h3')[0].text
    linea = replace_strings_trash_to_blank(linea)
    print(str(disenio) + " : " + linea)

    if re.search(regex_code, linea):
        data_name = value_null
        data_brand = value_null
        data_line = value_null
        data_code = re.findall(regex_code, linea)[0]
        if len(data_code[0]):
            data_code = data_code[0]
        elif len(data_code[1]):
            data_code = data_code[1]
        elif len(data_code[2]):
            data_code = data_code[2]
        elif len(data_code[3]):
            data_code = data_code[3]
        else:
            data_code = data_code[4]
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

        if re.search(" \d+[a-z]", linea):
            data_index_and_speed_rating = re.findall(" \d+[a-z]", linea)[0]
            linea = linea.replace(data_index_and_speed_rating, "")
            data_index = re.findall("\d+", data_index_and_speed_rating)[0]
            data_speed_rating = re.findall("[a-z]", data_index_and_speed_rating)[0]

        data_name = re.split(regex_code, linea)
        data_name.remove(data_code)
        for iterator_data_name in range(len(data_name)):
            if data_name[iterator_data_name] is not None and len(data_name[iterator_data_name]) != 0:
                data_name = data_name[iterator_data_name]
                break

        data_brand = prepare_string_to_db(re.findall("\w+", data_name)[0])
        data_name = prepare_string_to_db(data_name)
        if data_brand!=data_name:
            data_name = data_name.replace(data_brand, "")

        data_code = data_code.replace(" ", "").upper()

        data_comentario = disenios[disenio].find_elements(By.CLASS_NAME, 'prod-li-informations')[0].get_attribute("innerText")

        # info producto
        data_price_con_iva = float(prepare_string_to_price(
            prepare_string_to_db(disenios[disenio].find_elements(By.CLASS_NAME, tag_price)[0].text)))
        data_price_sin_iva = data_price_con_iva / factor_tax;
        data_original_con_iva = data_price_con_iva
        data_original_sin_iva = data_price_sin_iva
        data_price_con_iva_usd = data_price_con_iva / rate_exchange
        data_price_sin_iva_usd = data_price_sin_iva / rate_exchange

        print("brand : " + data_brand)
        print("name : " + data_name)
        print("code : " + data_code)
        print("index : " + data_index)
        print("index : " + data_speed_rating)
        print("comentario : " + data_comentario)
        print("data_price_con_iva : " + str(data_price_con_iva))
        print("data_price_sin_iva : " + str(data_price_sin_iva))
        print("data_original_con_iva : " + str(data_original_con_iva))
        print("data_original_sin_iva : " + str(data_original_sin_iva))
        print("data_price_sin_iva_usd : " + str(data_price_sin_iva_usd))
        print("data_price_con_iva_usd : " + str(data_price_con_iva_usd))

        # String query x element
        string_query = prepare_string_to_query(location_id, '"' + data_name + '"', '"' + data_brand + '"',
                                               '"' + data_code + '"', data_width, data_ratio, data_rim,
                                               data_original_sin_iva, data_original_con_iva,
                                               data_price_sin_iva, data_price_con_iva,
                                               data_price_sin_iva_usd, data_price_con_iva_usd,
                                               rate_exchange, rate_tax,
                                               data_index, '"' + data_speed_rating + '"',
                                               data_category,
                                               '"' + LINK_WEB + '"', disenio,
                                               value_null,
                                               timestamp_now)
        print(string_query)
        parciales.append(string_query)
    else:
        print("error : " + linea)

    print("\n")

if len(parciales):
    database = DataBase()
    database.parciales = parciales
    database.insert_register()

# Espera para cargar base y cerrar navegador
sleep(random_time(TIME_RANGE_LG))
driver.close()
