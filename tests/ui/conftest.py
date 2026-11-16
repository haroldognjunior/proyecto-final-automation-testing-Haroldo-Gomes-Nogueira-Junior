import pytest

from pages import InventoryPage, LoginPage
from utils.helpers import load_credentials


@pytest.fixture
def logged_driver(driver):
    """Navegador que ya pasó por el login (mismo fixture que en la pre-entrega)."""
    credentials = load_credentials()
    LoginPage(driver).open().login(credentials["username"], credentials["password"])
    return driver


@pytest.fixture
def inventory_page(logged_driver):
    """Página de inventario lista para usar. La usan casi todos los tests de UI."""
    return InventoryPage(logged_driver).wait_until_loaded()
