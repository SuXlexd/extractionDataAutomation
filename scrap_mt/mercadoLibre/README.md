![Tu Empresa](assets/espot2.png)

# Web Scraping Project 🚀

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## 📖 Descripción

Este proyecto está diseñado para realizar **web scraping** en Mercado Libre, enfocado en la recolección de datos relacionados con el mercado de llantas en México. El proceso consta de dos etapas principales: la recolección de enlaces de interés y el consumo de dichos enlaces para almacenar información relevante y capturas de pantalla.

---

## 🛠️ Características

- 🌐 **Extracción de datos estructurados**: Obtención de información detallada sobre llantas de las principales marcas comerciales en México.
- 🗂️ **Almacenamiento automatizado**: Los datos recolectados se almacenan en una base de datos estructurada. La definición de las tablas necesarias se encuentra en la carpeta `BDD`, y el archivo `.env` permite configurar el nombre de la base de datos.
- 📊 **Homologación de datos**: Proceso de normalización de datos para corregir inconsistencias o clasificaciones erróneas utilizando la herramienta de homologación proporcionada.
- 🔄 **Automatización parcial**: Si bien el sistema aún requiere intervención humana para iniciar los procesos de recolección y scraping, está diseñado para minimizar los esfuerzos manuales.

---

## 🚀 Cómo comenzar

### Prerrequisitos

- Python 3.8 o superior.
- Dependencias enumeradas en el archivo `requirements.txt`.

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/espot-mkt/meli-distribuited-scrap.git
   cd meli-distribuited-scrap
   pip install -r requirements.txt
   ```

2. Configura tu base de datos local asegurándote de incluir las tablas necesarias. El código SQL para la creación de estas tablas se encuentra en la carpeta `BDD`.

3. Define las variables de entorno necesarias para la ejecución del proyecto, según lo especificado en el archivo `.env` .

## 🧑‍💻 Instrucciones de uso

### Etapa 1: Recolección de enlaces

Ejecuta el siguiente comando para iniciar la recolección de enlaces:
    
   ```bash
    python .\main COLLECT {LOCAL,QUIKERY}
```

Donde:

- `LOCAL`: Indica que la operación se realizará utilizando una base de datos local configurada previamente.
- `QUIKERY`: Utiliza una base de datos remota alojada en la BDD del dominio Quikery.

### Etapa 2: Proceso de scraping

Para extraer datos de los enlaces recolectados, utiliza el siguiente comando:

```bash
    python .\main.py SCRAP {LOCAL, QUIKERY}
```
