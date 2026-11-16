"""
Defectos conocidos con el usuario problem_user.

Están marcados como xfail: el test describe el comportamiento CORRECTO,
y mientras el bug exista va a figurar como "xfailed" en el reporte
(no rompe la ejecución). Cada uno está vinculado a su BUG-ID del documento.
"""
import pytest

from pages import InventoryPage, LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def problem_inventory(driver):
    LoginPage(driver).open().login("problem_user", "secret_sauce")
    return InventoryPage(driver).wait_until_loaded()


@pytest.mark.xfail(reason="BUG-001: todas las imágenes del inventario son la misma")
def test_problem_user_product_images_are_different(problem_inventory):
    images = problem_inventory.get_image_sources()
    assert len(set(images)) == len(images), "Hay productos con la misma imagen"


@pytest.mark.xfail(reason="BUG-002: el orden por precio no cambia la lista")
def test_problem_user_sort_by_price(problem_inventory):
    problem_inventory.sort_by("Price (low to high)")
    prices = [p["price"] for p in problem_inventory.get_products()]
    assert prices == sorted(prices)


@pytest.mark.xfail(reason="BUG-003: el campo Last Name no guarda lo que se escribe")
def test_problem_user_checkout_last_name(problem_inventory):
    problem_inventory.add_first_product_to_cart()
    checkout = problem_inventory.go_to_cart().go_to_checkout()
    checkout.fill_customer_info("Haroldo", "Nogueira", "78700")

    assert checkout.get_field_value(checkout.LAST_NAME_INPUT) == "Nogueira"
