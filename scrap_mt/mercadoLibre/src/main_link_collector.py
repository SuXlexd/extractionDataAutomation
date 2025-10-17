from termcolor import colored
from .utils.const.links_and_brands import links_strings,brands
from .utils.procedures.prints import *
from .utils.webdriver.driver_factory import get_new_driver
from tabulate import tabulate
from .utils.wait import *
# from link_collector_fun import *
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
import sys



def main_link_collector(bdd_obj):
    links_to_explore=[]

    for brand_tuple in brands:
        for link in links_strings:
            new_link = link.format(brand_tuple[0])
            links_to_explore.append((new_link,brand_tuple[1],link))

    len_links_to_explore=len(links_to_explore)
    current=0
    print_magenta(f'Links a explorar: {len_links_to_explore}')
    try:
        driver=get_new_driver()
        pass
    except Exception as e:
        print_red('\n')
        print_red(e)
        print_red('\nERR: Driver no creado')

    products=0    


    no_repeat_links=[]

    for config in links_to_explore:
        link=config[0]
        brand=config[1]
        generator_link=config[2]
        print_magenta(f'Progress: {current}/{len_links_to_explore}')
        print_grey(f"Actual brand:{brand}")
        print_grey(f"Actual link:")
        print_grey(f"\t{link}")
        current+=1
        try:
            current_link_inserts=collect_link(no_repeat_links,link,brand,generator_link.format(brand),bdd_obj,driver)
            if(current_link_inserts):
                products+=current_link_inserts
            print_cyan(f'\n\t\t Inserciones a la base:{products}')

        except Exception as e:
            print_red('\n') 
            print_red(e)
            print_red('\nERR: No se pudo recolectar el link')
            wait_scrap(5,'Esperando por siguiente link...')
            
        


def clean_driver_meli(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(.,"Aceptar cookies")]').click()
    except Exception as e:
        pass
    try:
        driver.find_element(By.XPATH, '//span[contains(normalize-space(.),"Más tarde")]').click()
    except Exception as e:
        pass

def get_next_page(driver):
    try:
        btn=driver.find_element(By.CSS_SELECTOR,"li.andes-pagination__button.andes-pagination__button--next a.andes-pagination__link")
        driver.execute_script("""arguments[0].scrollIntoView({block: 'center', inline: 'center'});""", btn)
        sleep(30)
        btn=driver.find_element(By.CSS_SELECTOR,"li.andes-pagination__button.andes-pagination__button--next")
        btn.click()
        return True
    except Exception as e:
        print(e)
        return False



def collect_link(no_repeat_links,link,brand,generator_link,bdd_obj,driver):
    insert_querys=[]
    driver.get(link)
    wait_scrap(2,'Esperando para recolectar')
    clean_driver_meli(driver)
    
    try:
        for i in range(4):
            try:
                resultados=driver.find_element(By.CLASS_NAME, 'ui-search-search-result__quantity-results').text
                resultados_num=int(''.join(filter(str.isdigit, resultados)))
                break
            except StaleElementReferenceException:
                print_cyan('\n\n\t\tSUCEDE ERROR DESEADO')
                driver.refresh()
                wait_scrap(3, 'Esperando por pagina completa')
                continue
    except Exception as e:
        print_yellow('\tLink sin articulos disponibles')
        return
    
    productos=0
    query_str= "INSERT INTO links (link, revisado, marca, link_generador) VALUES (:link,:revisado,:marca,:link_generador)"
    
    

    while(True):
        for i in range(4):
            try:
                order_list= driver.find_element(By.XPATH, '//ol[contains(@class, "ui-search-layout")]')
                list_items=order_list.find_elements(By.TAG_NAME, 'li')
            except StaleElementReferenceException:
                print_cyan('\n\n\t\tSUCEDE ERROR DESEADO 2')
                driver.refresh()
                wait_scrap(2, 'Esperando por pagina completa')
                continue
            
        for li in list_items:
            try:
                a_element=li.find_element(By.XPATH, './/a[contains(@class, "poly-component__title")]')
            except:
                productos+=1
                continue
            href=a_element.get_attribute("href")
            content=a_element.text
            if(content in no_repeat_links):
                productos+=1
                continue
            else:
                insert_querys.append({'link': href, 'revisado':0,'marca':brand,'link_generador':generator_link})
                productos+=1
                no_repeat_links.append(content)
                progress = build_progress_bar_string("Recolectando configuracion actual", productos, resultados_num)
                print(f"\r{progress}", end="", flush=True)
        
        
        next=get_next_page(driver)
        if(next):
            # driver.get(next)
            wait_scrap(2,'Esperando para recolectar')
        else:
            if(insert_querys):
                bdd_obj.make_bulk_insert(query_str,insert_querys)
            return len(insert_querys)
            
        

    


    



            


        
    return resultados_num


    # layout_items = driver.find_element
        

    
    

    

if __name__ == "__main__":
    print('Hola')
    # Aqui van las pruebas para debugear