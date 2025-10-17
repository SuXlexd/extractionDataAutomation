from dotenv import load_dotenv
from src.utils.bdd.bdd_espot_scraping import BddEspotScraping
from src.utils.procedures.prints import *
from src.utils.procedures.create_screenshot_directory import create_screenshot_directory
from src.utils.procedures.get_env_variables import get_env_variables
from src.main_link_collector import main_link_collector
from src.main_link_scrap import main_scrap_meli
import argparse
import os
from datetime import datetime

def main():
    load_dotenv()
    INSTANCE_ID=os.getenv('INSTANCE_ID')
    
    #Recuperamos argumentos
    parser=argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('action', choices=['COLLECT', 'SCRAP'], help='Accion a realizar')
    parser.add_argument('bdd', choices=['LOCAL', 'QUIKERY'], help='Accion a realizar')
    args = parser.parse_args()
    print_green('OK: Argumentos parseados')

    #Creamos variables de entorno
    try:
        env_variables=get_env_variables(args.bdd.upper())
        host=env_variables['host']
        database=env_variables['database']
        user=env_variables['user']
        password=env_variables['password']
    except Exception as e:
        print_red('\n')
        print_red(e)
        print_red('\nERR: Variables de entorno no cargadas')

    print_green('OK: Variables de entorno cargadas')
        


    #Objeto bdd que va a realizar las inserciones
    try:
        bdd_obj=BddEspotScraping(database=database,host=host,user=user,password=password)
    except Exception as e:
        print_red('\n')
        print_red(e)
        print_red('\nERR: Objeto BddEspotScraping no se pudo crear')
    print_green('OK: Objeto BddEspotScraping creado')
    
    
    if(args.action.upper()=='COLLECT'):
        print_cyan('\nIniciando recoleccion de links...')
        main_link_collector(bdd_obj)

    if(args.action.upper()=='SCRAP'):
        print_cyan('\nInciando proceso de scrapeo...')
        create_screenshot_directory()
        main_scrap_meli(bdd_obj,INSTANCE_ID)
    
# Este bloque asegura que main() se ejecute solo si el archivo es ejecutado como un script
if __name__ == "__main__":
    main()
