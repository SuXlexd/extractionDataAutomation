# MrCobra Playwright Scraper

Este proyecto contiene un scraper en Python (`mrcobra_playwright.py`) que extrae información de llantas publicadas en [MrCobra MX](https://www.mrcobra.mx/listado/accesorios-vehiculos/llantas/llantas-motos/) utilizando la API síncrona de Playwright. El script recorre la paginación, abre cada producto y guarda los datos normalizados en una base de datos MySQL.

## Requisitos

- Python 3.10 o superior.
- Dependencias listadas en `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```
- Playwright necesita que se instale el navegador Chromium:
  ```bash
  playwright install chromium
  ```
- Base de datos MySQL accesible con credenciales válidas.

## Configuración

1. Crea un archivo `.env` en la raíz del repositorio (misma carpeta donde está `03_MrCobra/`) con las variables:
   ```
   HOST=HOST
   USER=USER
   PASSWORD=PASSWD
   DATABASE=DB
   ```
   El scraper rechaza la ejecución si falta alguna variable.

2. Verifica que la tabla `registers` en tu base de datos coincida con las columnas que usa el `INSERT` preparado del script (`location_id`, `name`, `brand`, `size`, etc.).

## Ejecución

1. Activa tu entorno virtual.
2. Desde la carpeta raíz del repositorio ejecuta:
   ```bash
   python 03_MrCobra/mrcobra_playwright.py
   ```
3. El script abrirá Chromium en modo visible, recorrerá la categoría, procesará cada producto y almacenará los resultados en lotes. El avance se muestra en consola.

## Comportamiento destacado

- **Playwright sync**: navega el listado, hace scroll para cargar todos los resultados y visita cada producto.
- **Normalización de datos**: extrae campos directamente de la tabla de especificaciones; si faltan, usa heurísticas basadas en el título para completar `name`, `brand` y `size`.
- **Persistencia por lotes**: agrupa 50 registros antes de ejecutar el `INSERT` para reducir la carga sobre MySQL. Imprime cualquier registro que falle durante la inserción.
- **Tiempo de espera aleatorio**: introduce pequeñas pausas aleatorias para simular navegación humana.

## Notas adicionales

- Ajusta las constantes de configuración (por ejemplo `LOCATION_ID`, rangos de sleep o tamaño de lote) según tus necesidades.
- Si el sitio presenta desafíos (captcha, errores) el script registra mensajes en consola y continúa con el siguiente elemento.
- El navegador se cierra automáticamente al finalizar, pero puedes forzar la salida con `Ctrl+C` si necesitas detener el scraping.

