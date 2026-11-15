"""
Funciones auxiliares del framework.

Viene de la pre-entrega: ahí este archivo tenía todo (login, carrito, etc.).
Con Page Object Model esas acciones pasaron a pages/, y aquí quedó
lo que no pertenece a ninguna página: el navegador, los datos y las capturas.
"""
import csv
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

from selenium import webdriver

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "datos"
SCREENSHOTS_DIR = PROJECT_ROOT / "reports" / "screenshots"

log = logging.getLogger(__name__)


# ---------- Navegador ----------

def create_driver():
    """Crea una instancia de Chrome. Con HEADLESS=1 corre sin ventana."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,900")

    # Chrome muestra un aviso de "contraseña filtrada" con secret_sauce
    # y tapa la página; con esto se desactiva.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        # Necesarios para que Chrome arranque dentro del contenedor de GitHub Actions
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # Desde Selenium 4.6 no hace falta descargar chromedriver a mano
    driver = webdriver.Chrome(options=options)
    log.info("Chrome iniciado (headless=%s)", os.getenv("HEADLESS") == "1")
    return driver


# ---------- Datos de prueba ----------

def load_credentials(user_key="standard"):
    """Igual que en la pre-entrega: el usuario base sale de datos/usuarios.json."""
    return read_json("usuarios.json")[user_key]


def read_json(file_name):
    with open(DATA_DIR / file_name, encoding="utf-8") as file:
        return json.load(file)


def read_csv(file_name):
    """Devuelve las filas del CSV como lista de diccionarios (una fila = un caso)."""
    with open(DATA_DIR / file_name, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


# ---------- Evidencias ----------

def save_screenshot(driver, test_name):
    """Guarda una captura con el nombre del test y la fecha/hora."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    # Los tests parametrizados tienen [] en el nombre, los limpio para el archivo
    safe_name = re.sub(r"[^\w\-]", "_", test_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = SCREENSHOTS_DIR / f"{safe_name}_{timestamp}.png"
    driver.save_screenshot(str(file_path))
    log.error("Test fallido, captura guardada en %s", file_path)
    return file_path
