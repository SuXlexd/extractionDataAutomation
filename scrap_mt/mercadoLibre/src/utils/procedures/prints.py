from termcolor import colored
from tabulate import tabulate

def print_colored(s,color):
    print(colored(s,color))

colored('hoila','grey')
def print_blue(s):
    print_colored(s,'blue')

def print_cyan(s):
    print_colored(s,'cyan')

def print_green(s):
    print_colored(s,'green')

def print_grey(s):
    print_colored(s,'grey')

def print_magenta(s):
    print_colored(s,'magenta')

def print_red(s):
    print_colored(s,'red')

def print_yellow(s):
    print_colored(s,'yellow')


def print_info(datos):
    """
    Imprime información en forma de tabla con colores diferentes para la etiqueta y el valor.
    
    :param datos: Lista de tuplas con la forma (etiqueta, valor, color_etiqueta, color_valor)
    """
    # Crea una lista de filas con colores aplicados
    tabla = []
    for etiqueta, valor, color_etiqueta, color_valor in datos:
        etiqueta_coloreada = colored(etiqueta, color_etiqueta, attrs=["bold"])
        valor_coloreado = colored(valor, color_valor)
        tabla.append([etiqueta_coloreada, valor_coloreado])

    # Imprime la tabla usando tabulate
    print(tabulate(tabla, headers=["Dato", "?"], tablefmt="github"))