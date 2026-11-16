"""
Login con distintos usuarios.

En la pre-entrega probaba solo standard_user. Aquí los casos salen de
datos/login_users.csv: para probar otro usuario basta con agregar una fila.
"""
import pytest

from pages import InventoryPage, LoginPage
from utils.helpers import read_csv

pytestmark = pytest.mark.ui

LOGIN_CASES = read_csv("login_users.csv")
VALID_LOGINS = [case for case in LOGIN_CASES if case["expected_result"] == "ok"]
INVALID_LOGINS = [case for case in LOGIN_CASES if case["expected_result"] == "error"]


@pytest.mark.parametrize("case", VALID_LOGINS, ids=lambda c: f"{c['case_id']}-{c['username']}")
def test_login_with_valid_users(driver, case):
    LoginPage(driver).open().login(case["username"], case["password"])
    inventory = InventoryPage(driver).wait_until_loaded()

    assert "/inventory.html" in driver.current_url, f"No redirigió al inventario: {driver.current_url}"
    assert inventory.get_logo_text() == "Swag Labs"
    assert inventory.get_title() == "Products"


@pytest.mark.parametrize("case", INVALID_LOGINS, ids=lambda c: c["case_id"])
def test_login_invalid_shows_error(driver, case):
    login_page = LoginPage(driver).open()
    login_page.login(case["username"], case["password"])

    error = login_page.get_error_message()
    assert error == case["expected_message"], f"Mensaje inesperado: '{error}'"
    # El mensaje solo no alcanza: también confirmo que no entró
    assert "/inventory.html" not in driver.current_url, "No debería haber entrado al inventario"
