import re
from playwright.sync_api import Page, expect
import asyncio, time, random, urllib.robotparser as rp
from playwright.sync_api import sync_playwright




# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
#              "(KHTML, like Gecko) Chrome/120 Safari/537.36"

#GOOGLE BOT
USER_AGENT= "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
            "Chrome/137.0.0.0 Safari/537.36 (compatible; Google-Read-Aloud; +https://support.google.com/webmasters/answer/1061943)"



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent=USER_AGENT)
    page = context.new_page()

    # Navigate explicitly, similar to entering a URL in the browser.
    page.goto('https://www.mrcobra.mx/listado/accesorios-vehiculos/llantas/llantas-motos/')
    time.sleep(random.uniform(1, 3))  # Espera aleatoria entre 5 y 10 segundos
print(page.url)



