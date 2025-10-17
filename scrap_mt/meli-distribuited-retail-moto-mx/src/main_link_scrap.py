from src.utils.webdriver.driver_factory import get_new_driver
from src.utils.webdriver.webdriver_procedures import *
from src.utils.api.api_banxico import precio_dolar
from src.utils.procedures.prints import *
from src.utils.wait import wait

import functools
import operator
import re

import time


def seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}:{minutes}:{seconds}"

# Se agrega parche para extraer size de la llanta del título en caso de que no esté en la tabla de especificaciones
def extract_size_from_title(text):
    """Return the first tire size found in the given text."""
    if not text:
        return None

    patterns = [
        r'(?:LT|ST|P)?\d{3}/\d{2}(?:[A-Z]{0,2})?\s?R\s?\d{2}',  # 215/65R16, P215/65R16, 225/45ZR17
        r'\d{2}X\d{2}(?:\.\d{1,2})?\s?R\s?\d{2}',              # 33X12.5R15, 31X10.50R15
        r'(?:LT|ST|P)?\d{3}/\d{2}-\d{2}',                          # 215/65-16
        r'(?:LT|ST|P)?\d{3}/\d{2}/\d{2}',                          # 215/65/16
    ]

    normalized = text.upper()
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            value = re.sub(r'\s+', '', match.group(0))
            if value.count('/') == 2 and 'R' not in value:
                parts = value.split('/')
                if len(parts) == 3:
                    value = f"{parts[0]}/{parts[1]}R{parts[2]}"
            if '-' in value and 'R' not in value:
                value = value.replace('-', 'R', 1)
            return value
    return None


def main_scrap_meli(bdd_obj, instance_id):
    scrap_index=0
    dolar_price=precio_dolar()
    consumed_links=0
    links_per_cycle=10
    start_time=time.time()
    current_time=time.time()
    driver=get_new_driver()
    while True:
        ids_to_update,links=bdd_obj.getLinks(links_per_cycle)
        consumed_links+=links_per_cycle
        remaining_links=bdd_obj.getRemainingLinks()
        if(remaining_links==0):
            print_green(f"Links completamente consumidos, tiempo de ejecucion: {current_time}")
            print_green(f"Links totales scrapeados: {scrap_index}")
            if(scrap_index!=0):
                print_green(f"Tiempo promedio por link: {round(current_time/scrap_index,0)}")
            print_green(f"Links reales consumidos: {consumed_links}")
            print_green(f"Links fallidos: {consumed_links-scrap_index}")
            break
        links_to_scrape=[l[1] for l in links]
        inserts=[]
        for index,link in enumerate(links_to_scrape):
            #q=meli_scrap_link(link,dolar_price,driver,scrap_index=0, retries=3, wait_time=6)
            q=meli_scrap_link(link,dolar_price,driver,scrap_index=0, retries=3, wait_time=5)
            if q:
                inserts.append(q)
                scrap_index+=1
            end_time=time.time()
            current_time=round(end_time-start_time,2)
            datos = [
                        ('Links scrapeados exitosamente', scrap_index, 'green', 'green'),
                        ('Links consumidos', consumed_links, 'yellow', 'yellow'),
                        ('Links fallidos', consumed_links-scrap_index, 'red', 'red'),
                        ('Links faltantes en este ciclo', links_per_cycle - index - 1, 'cyan', 'magenta'),
                        ('Tiempo transcurrido', seconds_to_hhmmss(current_time), 'cyan', 'magenta'),
                        ('Segundos por link', current_time // scrap_index if scrap_index != 0 else current_time, 'cyan', 'magenta'),
                        ('Links faltantes en BDD', f"{remaining_links:,}", 'cyan', 'magenta'),
                        ('TIEMPO ESTIMADO PARA FINALIZAR', seconds_to_hhmmss((current_time / scrap_index) * remaining_links) if scrap_index != 0 else 'N/A', 'cyan', 'magenta')
                    ]
            print_info(datos)
        
        try:
            bdd_obj.makeInserts(inserts)
            bdd_obj.confirmLinks(ids_to_update)
        except:
            print_red(f'Imposible insertar {len(inserts)} registros.')
            continue



def meli_scrap_link(link,dolar_price,driver,scrap_index=0,retries=3,wait_time=4):
    RATE_EXCHANGE = dolar_price
    RATE_TAX=0.16
    val_init_q = '`location_id`, `price_og_fr`, `price_og_tx`, `price_mn_fr`, `price_mn_tx`,`price_us_fr`,' \
    '`price_us_tx`,`rate_exchange`, `rate_tax`, `stock` , `scrap_link`, `scrap_index`,'  \
    '`created_at`,`updated_at`, `comment`, `store`,`ss`'
    #Cargamos el link:
    try:
        driver_ready=until_complete(link,driver,retries=retries,wait_time=wait_time)
        if not driver_ready:
            return ""
        if isPaused(driver):
            wait(wait_time,'dots',"Esperando para scrapear...", bar=True, percentage=False, seconds=True, clear=True)
            return ""
    except Exception as e:
        print_red('\n')
        print_red('ERROR OCURRIDO EN meli_scrap_link')
        print_red('\n')
        print_red(e)
        print_red(f'\nERR: Link corrupto {link}')
        return ""
    
    wait(wait_time,'dots',"Esperando para scrapear...", bar=True, percentage=False, seconds=True, clear=True)

    #Recuperamos toda la informacion posible con las funciones definidas
    precioOriginal, precioVenta=getPrecios(driver)
    if(precioOriginal==0 and precioVenta==0):
        return ""
    titulo = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]').text
    titulo = titulo.replace('"', '').replace("'", '').upper()
    size_from_title = extract_size_from_title(titulo)
    disponibles=getStock(driver)
    store=getStore(driver)
    #Especificaciones de la llanta:
    spec = driver.find_elements(
        By.XPATH, '//th[@class="andes-table__header andes-table__header--left ui-vpp-striped-specs__row__column ui-vpp-striped-specs__row__column--id"]')
    #Valores especificados a la llanta:
    values = driver.find_elements(
        By.XPATH, '//td[@class="andes-table__column andes-table__column--left andes-table__column--vertical-align-center ui-vpp-striped-specs__row__column"]')
    spec = list(map(extr, spec))
    values = list(map(extr, values))
    spec_value=dict(zip(spec,values))
    vehicle_type = spec_value.get('Tipo de vehículo')
    # Parche para descartar llantas que no sean de moto, ignora estos productos y no scrapea
    if vehicle_type:
        normalized_vehicle = vehicle_type.upper()
        if 'MOTO' not in normalized_vehicle:
            print_yellow(f"Producto omitido (no moto): {titulo}")
            return ""
    if (not spec_value.get('Tamaño')) and size_from_title:
        spec_value['Tamaño'] = size_from_title  # Parche para asignar tamaño desde el título si no está en especificaciones (fallback)
    if not spec_value.get('Tamaño'):
        return ""  # Si aún no hay tamaño, descartamos el producto
    nombre, nt, cols, vals = string_query(spec_value)
    try:
        precioO= float(precioOriginal.replace(",", ""))/nt
        precio = float(precioVenta.replace(",", ""))/nt
    except:
        return ""
    price_og_fr = float(precioO)-(float(precioO)*RATE_TAX)
    price_og_tx = float(precioO)
    price_mn_fr = float(precio)-(float(precio)*RATE_TAX)
    price_mn_tx = float(precio)
    price_us_fr = float(price_mn_fr)/RATE_EXCHANGE
    price_us_tx = float(price_mn_tx)/RATE_EXCHANGE
    # ss_name=screenshot(link,nombre)
    ss_name="no_ss"
    fecha_actual = datetime.now()
    date = fecha_actual.strftime("%Y-%m-%d")
    if(ss_name!='error'):
        specs_init_q = "'3','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'".format(price_og_fr, price_og_tx, 
                                                                                                        price_mn_fr, price_mn_tx, 
                                                                                                        price_us_fr, price_us_tx,
                                                                                                        str(RATE_EXCHANGE), str(RATE_TAX), disponibles, 
                                                                                                        link, scrap_index, date, date,
                                                                                                        titulo, store, ss_name)
        query = 'INSERT INTO `registers` ('+ val_init_q + cols +') VALUES (' + specs_init_q + vals +')'
        return query
    else:
        print(colored('Error general','red'))
        return ""
    

def string_query(specs):
    ml_to_db = {
        'Marca': 'brand',
        'Modelo': 'name',
        'Tamaño': 'size',
        'Cantidad de Llantas': 'number_tires',
        'Cantidad de llantas': 'number_tires',
        'Índice de carga': 'load_index',
        'Índice de velocidad': 'speed_rating',
        'Ancho de sección': 'size_width',
        'Relación de aspecto': 'size_ratio',
        'Diámetro del rin': 'size_rim',
        'UTQG': 'utqg',
        'Tipo de terreno': 'perf',
        'Tipo de construcción': 'constr',
        'Tipo de vehículo': 'category',
    }

    cols = ""
    vals = ""
    nt = 1
    modelo = specs.get('Modelo') or "modelo"
    linea = specs.get('Línea')
    if linea and modelo and linea.upper() not in modelo.upper():
        modelo = f"{modelo} {linea}"
    medida = specs.get('Tamaño') or "medida"

    added_columns = set()

    for key, column in ml_to_db.items():
        valor = specs.get(key)
        if not valor or column in added_columns:
            continue

        valor = str(valor).strip() 

        if column in ['size_width', 'size_ratio', 'size_rim']:
            numeric_value = ''.join(ch for ch in valor if ch.isdigit() or ch == '.')
            if not numeric_value:
                continue
            valor = numeric_value
        #Limpiamos load_index dejando solo numeros en vez de texto    
        if column == 'load_index':
            digits = ''.join(ch for ch in valor if ch.isdigit())
            if not digits:
                continue
            valor = digits

        if column == 'number_tires':
            try:
                nt = int(valor)
            except ValueError:
                pass
        if column == 'speed_rating':
            valor = str(valor).strip()[:1]
        if column in ('perf', 'constr'):
            valor = str(valor)[:5]

        valor = str(valor).strip().upper()
        if not valor:
            continue

        cols += f",`{column}`"
        vals += f",'{valor}'"
        added_columns.add(column)

    nombre = f"{modelo}-{medida}".replace(".", "").replace(" ", "_").replace("/", "-")

    return nombre, nt, cols, vals
