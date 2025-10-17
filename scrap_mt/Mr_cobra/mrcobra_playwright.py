"""
Scraper for MrCobra MX rewritten to use Playwright's sync API.
Con fallback desde el título para completar name/brand/size si faltan.
"""

from __future__ import annotations

import datetime
import os
import random
import re
from dataclasses import dataclass
from time import sleep
from typing import List, Optional, Sequence, Tuple

import pymysql
from dotenv import load_dotenv, find_dotenv
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

# ========= Config =========
RATE_EXCHANGE = 19.4504
RATE_TAX = 16
FACTOR_TAX = RATE_TAX / 100 + 1
LOCATION_ID = 3
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_BATCH_SIZE = 50

# Carga variables .env respetando rutas relativas al proyecto.
load_dotenv(find_dotenv(usecwd=True), override=True)

def _env_required(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Variable de entorno requerida no encontrada: {name}")
    return value.strip()

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/137.0.0.0 Safari/537.36 (compatible; Google-Read-Aloud;"
    " +https://support.google.com/webmasters/answer/1061943)"
)

LINK_WEB = "https://www.mrcobra.mx/listado/accesorios-vehiculos/llantas/llantas-motos/"
ITEM_READY = "/html/body/main/div/div[2]/section"
ITEM_READY_PAG = "/html/body"
TAG_TIRE = "ui-search-layout__item"
MAX_SCROLL_ITERATIONS = 10

SQL_HOST = _env_required("HOST")
SQL_USER = _env_required("USER")
SQL_PASSWORD = _env_required("PASSWORD")
SQL_DB = _env_required("DATABASE")

TIME_RANGE_SM: Tuple[float, float] = (0.5, 1)
TIME_RANGE_MD: Tuple[float, float] = (0.5, 1)
TIME_RANGE_LG: Tuple[float, float] = (0.5, 1)

# Insersion a la BD
# Prepared statement para lotes de inserción en `registers`.
SQL_INSERT = (
    "INSERT INTO `registers` (`location_id`, `name`, `brand`, `size`, `size_width`,"
    " `size_ratio`, `size_rim`, `price_og_fr`, `price_og_tx`, `price_mn_fr`,"
    " `price_mn_tx`, `price_us_fr`, `price_us_tx`, `rate_exchange`, `rate_tax`,"
    " `load_index`, `speed_rating`, `category`, `scrap_link`, `scrap_index`,"
    " `created_at`, `updated_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,"
    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

HTML_BREAK_PATTERN = re.compile(r"<br\s*/?>", re.IGNORECASE)
NUMBER_PATTERN = re.compile(r"[\d.]+")

# Patrones de medida comunes (ej. 120/80-16, 120/80 R16, 2.75-18).
SIZE_PATTERNS = [
    re.compile(r"\b\d{2,3}/\d{2,3}\s*(?:-\s*|\s*R\s*)\d{2,3}\b", re.IGNORECASE),
    re.compile(r"\b\d{1,2}(?:\.\d+)?\s*-\s*\d{2,3}\b", re.IGNORECASE),
    re.compile(r"\b\d{2,3}\s*R\s*\d{2,3}\b", re.IGNORECASE),
]

# ========= Heurísticas de parsing desde título =========
LOAD_SPEED_PATTERN = re.compile(r"\b(?P<load>\d{1,3})(?P<speed>[A-Z]{1,2})\b")
STOPWORDS = {
    "llanta", "llantas", "uso", "sin", "con", "camara", "cámara", "para", "moto",
    "delantera", "trasera", "tubeless", "tubetype", "tt", "tl", "de", "y", "en"
}
KNOWN_BRANDS = {
    "MICHELIN","PIRELLI","DUNLOP","TIMSUN","METZELER","BRIDGESTONE","CST","KENDA",
    "MAXXIS","IRC","AVON","CONTINENTAL","HEIDENAU","SHINKO","HUTCHINSON","CORDIAL","CORSA"
}
BRAND_PATTERN = re.compile(r"\b[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9\-]{2,}\b")

@dataclass
class ProductDetails:
    tire: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    size_width: Optional[str] = None
    size_ratio: Optional[str] = None
    size_rim: Optional[str] = None
    load_index: Optional[str] = None
    speed_rating: Optional[str] = None
    category: Optional[str] = None
    count: Optional[int] = None

@dataclass
class PriceInfo:
    mxn_with_tax: float
    mxn_without_tax: float
    usd_with_tax: float
    usd_without_tax: float

# ========= DB =========
class Database:
    """Contexto simple para manejar la conexión MySQL y lotes."""
    def __init__(self) -> None:
        self.connection = pymysql.connect(
            host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB
        )
        self.cursor = self.connection.cursor()
        print("Conexión establecida exitosamente!")

    def insert_products(self, records: Sequence[Tuple]) -> None:
        if not records:
            return
        try:
            self.cursor.executemany(SQL_INSERT, records)
            self.connection.commit()
        except Exception as exc:
            print(f"Error al insertar registros: {exc}")
            for record in records:
                print(f"  Registro fallido: {record}")
            raise
    
    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

# ========= Utils =========
def random_delay(time_range: Tuple[float, float]) -> float:
    return random.uniform(time_range[0], time_range[1])

def to_upper(value: Optional[str]) -> Optional[str]:
    return value.upper() if value else None

def clean_html_text(raw: Optional[str]) -> Optional[str]:
    if raw is None:
        return None
    text = raw.replace("&NBSP;", " ").replace("&nbsp;", " ")
    text = HTML_BREAK_PATTERN.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text or None

def extract_number(value: Optional[str], pattern: Optional[re.Pattern] = None) -> Optional[str]:
    if not value:
        return None
    matcher = pattern or NUMBER_PATTERN
    match = matcher.search(value)
    return match.group(0) if match else None

def parse_price(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    normalized = value.replace("$", "").replace(",", "").replace(" ", "")
    try:
        return float(normalized)
    except ValueError:
        return None

def wait_for_xpath(page: Page, xpath: str, timeout: int = 5000) -> None:
    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
    except PlaywrightTimeoutError:
        print(f"Selector no encontrado dentro del tiempo: {xpath}")

def scroll_page(page: Page, max_attempts: int, stop_selector: Optional[str]) -> None:
    for _ in range(max_attempts):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        sleep(random_delay(TIME_RANGE_MD))
        if stop_selector and page.locator(stop_selector).count() > 0:
            break


# ========= Listado =========
def collect_listing_urls(page: Page) -> List[str]:
    """Recorre la paginación y acumula enlaces de productos sin duplicados."""
    product_urls: List[str] = []
    seen_products = set()
    visited_listing_pages = set()
    next_page_url = LINK_WEB

    while next_page_url and next_page_url not in visited_listing_pages:
        visited_listing_pages.add(next_page_url)
        try:
            page.goto(next_page_url, wait_until="domcontentloaded", timeout=45000)
        except PlaywrightTimeoutError:
            print(f"Timeout cargando listado: {next_page_url}")
            break

        wait_for_xpath(page, ITEM_READY)
        sleep(random_delay(TIME_RANGE_SM))
        scroll_page(page, MAX_SCROLL_ITERATIONS, ".andes-pagination")

        cards = page.locator(f".{TAG_TIRE}")
        count = cards.count()
        for index in range(count):
            anchors = cards.nth(index).locator("a")
            if anchors.count() == 0:
                continue
            href = anchors.first.get_attribute("href")
            if href and href not in seen_products:
                seen_products.add(href)
                product_urls.append(href)

        pagination_next = page.locator(".andes-pagination__button--next a")
        if pagination_next.count() == 0:
            break

        href_next = pagination_next.first.get_attribute("href")
        if not href_next or href_next in visited_listing_pages:
            break

        next_page_url = href_next
        sleep(random_delay(TIME_RANGE_MD))

    return product_urls

# ========= Detalle (tabla) =========
def parse_product_details(page: Page) -> ProductDetails:
    """Lee la tabla de especificaciones para poblar campos directos."""
    details = ProductDetails()
    tables = page.locator("tbody")

    for table_index in range(tables.count()):
        rows = tables.nth(table_index).locator("tr")
        for row_index in range(rows.count()):
            row = rows.nth(row_index)
            header_cells = row.locator("th")
            value_cells = row.locator("td span")

            if header_cells.count() == 0 or value_cells.count() == 0:
                continue

            header = clean_html_text(header_cells.first.inner_html())
            value = clean_html_text(value_cells.first.inner_html())

            if not header or value is None:
                continue

            if header == "Modelo":
                details.tire = to_upper(value)
            elif header == "Marca":
                details.brand = to_upper(value)
            elif header == "Tamaño":
                details.size = to_upper(value)
            elif header == "Cantidad de llantas":
                number = extract_number(value)
                if number:
                    try:
                        details.count = int(float(number))
                    except ValueError:
                        details.count = None
            elif header == "Índice de carga":
                details.load_index = extract_number(value)
            elif header == "Índice de velocidad":
                details.speed_rating = to_upper(value)
            elif header == "Estilo":
                details.category = to_upper(value)
            elif header == "Ancho de sección":
                details.size_width = extract_number(value)
            elif header == "Relación de aspecto":
                ratio = extract_number(value)
                if ratio:
                    details.size_ratio = ratio
            elif header == "Diámetro del rin":
                details.size_rim = extract_number(value)

    return details

# ========= Fallback desde el título =========
def get_title_text(page: Page) -> Optional[str]:
    xpath_candidates = [
        "//h1[contains(@class, 'ui-pdp-title__main-title')]",
        "//h1[contains(@class, 'ui-pdp-title')]",
        "//h1[contains(@class, 'product-title')]",
        "//h1",
    ]
    for xpath in xpath_candidates:
        locator = page.locator(f"xpath={xpath}")
        if locator.count() == 0:
            continue
        text = clean_html_text(locator.first.inner_text())
        if text:
            return text
    return None


def extract_size_from_text(text: str) -> Tuple[Optional[str], Optional[Tuple[int, int]]]:
    for pattern in SIZE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        normalized = re.sub(r"\s+", "", match.group(0)).upper()
        normalized = normalized.replace("R", "-")
        normalized = normalized.replace("--", "-")
        return normalized, match.span()
    return None, None

def detect_brand_from_title(title: str, after_size_span: Optional[Tuple[int, int]]) -> Optional[str]:
    """Heurística de marca cuando la tabla no la publica."""
    upper_title = title.upper()

    # 1) si viene una marca conocida, úsala
    for brand in KNOWN_BRANDS:
        if re.search(rf"\b{re.escape(brand)}\b", upper_title, flags=re.IGNORECASE):
            return brand

    # 2) si detectamos tamaño, toma la primera palabra relevante a partir de ahí
    if after_size_span:
        end = after_size_span[1]
        tail = upper_title[end:]
        for match in BRAND_PATTERN.finditer(tail):
            token = match.group(0)
            if token.lower() not in STOPWORDS:
                return token

    # 3) fallback: scan completo del título
    for match in BRAND_PATTERN.finditer(upper_title):
        token = match.group(0)
        if token.lower() not in STOPWORDS:
            return token

    return None

def fill_from_title_if_missing(details: ProductDetails, title: Optional[str]) -> None:
    if not title:
        return
    original_title = title
    title_up = title.upper()
    original_size_text = None

    # Tamaño (y span de posiciones para extraer brand después)
    size_value, size_span = extract_size_from_text(title_up)
    if size_span:
        original_size_text = original_title[size_span[0]:size_span[1]]
    if details.size is None and size_value:
        details.size = size_value

    # Descomponer tamaño en W/R/RIM si no vinieron
    if details.size:
        parts = details.size.split("-")
        if len(parts) == 2:
            width_part = parts[0]  # ej "120/80" o "2.75"
            rim_part = parts[1]
            if details.size_width is None:
                w = re.sub(r"[^\d.]", "", width_part.split("/")[0])
                details.size_width = w if w else None
            if details.size_ratio is None and "/" in width_part:
                r = re.sub(r"[^\d.]", "", width_part.split("/")[1])
                details.size_ratio = r if r else None
            if details.size_rim is None:
                rim = re.sub(r"[^\d.]", "", rim_part)
                details.size_rim = rim if rim else None

    # Marca
    if details.brand is None:
        brand = detect_brand_from_title(title, size_span)
        if not brand:
            brand = "SIN MARCA"
        details.brand = brand

    # índices carga/velocidad si faltan
    if details.load_index is None or details.speed_rating is None:
        for m in LOAD_SPEED_PATTERN.finditer(title_up):
            load = m.group("load")
            speed = m.group("speed")
            # evita confundir códigos de modelo tipo "TS-659F"
            if load and speed and len(speed) in (1, 2):
                if details.load_index is None:
                    details.load_index = load
                if details.speed_rating is None:
                    details.speed_rating = speed[:1]  # tu DB acepta 1 char
                break

    # Modelo/name: quitar llanta/brand/size/frasess y códigos -> resto = modelo
    if details.tire is None:
        model_text = original_title

        # quitar "Llanta(s) "
        model_text = re.sub(r"(?i)^llantas?\s+", "", model_text)

        # quitar tamaño detectado
        if details.size:
            model_text = re.sub(re.escape(details.size), "", model_text, flags=re.IGNORECASE)
        if original_size_text:
            model_text = model_text.replace(original_size_text, "")

        # quitar marca detectada
        if details.brand:
            model_text = re.sub(rf"\b{re.escape(details.brand)}\b", "", model_text, flags=re.IGNORECASE)

        # quitar frases comunes
        model_text = re.sub(r"(?i)uso\s+(sin|con)\s+c[áa]mara|tubeless|tubetype|para\s+moto|delantera|trasera", "", model_text)

        # quitar códigos carga/velocidad & PR
        model_text = re.sub(r"\b\d{1,3}[A-Z]{1,2}\b", "", model_text)  # 60S, 41P
        model_text = re.sub(r"\b\d{1,2}PR\b", "", model_text)          # 4PR, 6PR

        # limpiar & mayúsculas
        model_text = re.sub(r"\s+", " ", model_text).strip()
        details.tire = model_text.upper() if model_text else original_title.upper()

    # speed_rating a 1 char
    if details.speed_rating:
        details.speed_rating = details.speed_rating[:1]

    # fallbacks finales para evitar nulos críticos
    if details.size is None:
        details.size = "SIN TAMANO"
    if details.brand is None:
        details.brand = "SIN MARCA"

# ========= Precio =========
def extract_price_data(page: Page, count: Optional[int]) -> Optional[PriceInfo]:
    fractions = page.locator(".andes-money-amount__fraction")
    if fractions.count() == 0:
        return None

    raw_price = clean_html_text(fractions.first.inner_text())
    cents_locator = page.locator(".andes-money-amount__cents")

    if cents_locator.count():
        cents_text = clean_html_text(cents_locator.first.inner_text())
        if cents_text:
            raw_price = f"{raw_price}.{cents_text}"

    price_value = parse_price(raw_price)
    if price_value is None:
        return None

    units = count if count and count > 0 else 1
    per_unit_price = price_value / units
    price_without_tax = per_unit_price / FACTOR_TAX

    return PriceInfo(
        mxn_with_tax=round(per_unit_price, 2),
        mxn_without_tax=round(price_without_tax, 2),
        usd_with_tax=round(per_unit_price / RATE_EXCHANGE, 2),
        usd_without_tax=round(price_without_tax / RATE_EXCHANGE, 2),
    )

def _to_float_or_none(x: Optional[str]) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except:
        return None

def build_record(details: ProductDetails, price: PriceInfo, url: str, timestamp: str) -> Tuple:
    # casteos suaves para columnas float en BD
    size_width = _to_float_or_none(details.size_width)
    size_ratio = _to_float_or_none(details.size_ratio)
    size_rim = _to_float_or_none(details.size_rim)

    # Nota: aquí uso el mismo precio como og/mn; ajusta si manejas lógica distinta
    return (
        LOCATION_ID,
        details.tire,
        details.brand,
        details.size,
        size_width,
        size_ratio,
        size_rim,
        price.mxn_without_tax,   # price_og_fr
        price.mxn_with_tax,      # price_og_tx
        price.mxn_without_tax,   # price_mn_fr
        price.mxn_with_tax,      # price_mn_tx
        price.usd_without_tax,   # price_us_fr
        price.usd_with_tax,      # price_us_tx
        RATE_EXCHANGE,
        RATE_TAX,
        int(details.load_index) if details.load_index and details.load_index.isdigit() else None,
        details.speed_rating,
        details.category,
        url,
        0,
        timestamp,
        timestamp,
    )

# ========= Orquestación por producto =========
def scrape_product_page(page: Page, url: str, timestamp: str) -> Optional[Tuple]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except PlaywrightTimeoutError:
        print(f"Timeout cargando producto: {url}")
        return None

    sleep(random_delay(TIME_RANGE_SM))

    if "Internal Server Error" in page.title():
        print(f"Internal Server Error en producto: {url}")
        return None

    wait_for_xpath(page, ITEM_READY_PAG)
    scroll_page(page, MAX_SCROLL_ITERATIONS, ".nav-tools-footer")

    details = parse_product_details(page)

    # Fallback desde título para completar obligatorios
    title_text = get_title_text(page)
    fill_from_title_if_missing(details, title_text)

    # Validaciones duras: evita 1048 en DB
    if not details.tire or not details.brand or not details.size:
        print(f"[OMITIDO] Faltan campos obligatorios (name/brand/size) en: {url}")
        print(f"  title='{title_text}' parsed={details}")
        return None

    price_info = extract_price_data(page, details.count)
    if price_info is None:
        print(f"Precio no encontrado en producto: {url}")
        return None

    return build_record(details, price_info, url, timestamp)

# ========= Main =========
def run() -> None:
    timestamp_now = datetime.datetime.now().strftime(DATE_FORMAT)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        product_urls = collect_listing_urls(page)
        print(f"Total de productos detectados: {len(product_urls)}")

        batch: List[Tuple] = []
        with Database() as database:
            for index, product_url in enumerate(product_urls, start=1):
                print(f"Procesando ({index}/{len(product_urls)}): {product_url}")
                record = scrape_product_page(page, product_url, timestamp_now)
                if record is None:
                    continue

                batch.append(record)
                if len(batch) >= SQL_BATCH_SIZE:
                    database.insert_products(batch)
                    batch.clear()

            if batch:
                database.insert_products(batch)

        sleep(random_delay(TIME_RANGE_LG))
        page.close()
        context.close()
        browser.close()

if __name__ == "__main__":
    run()
