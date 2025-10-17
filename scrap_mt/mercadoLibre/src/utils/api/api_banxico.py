import requests
from datetime import date, timedelta

TOKEN = '5d25fa5788a36bbbb83f40633a2ac1da2d0d3a22529d0108076b4588a26b2a8c'

def precio_dolar():
    serie = 'SF63528'
    try:
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
        headers = {'Bmx-Token':TOKEN}
        response = requests.get(url, headers=headers)
        raw_data = response.json()
        if response.status_code == 200:
            data = response.json()
            serie = data.get('bmx', {}).get('series', [])[0]
            dato = serie.get('datos', [])[0]
            valor = dato.get('dato')
        else:
            valor=20
    except:
        valor=20
    return float(valor)
