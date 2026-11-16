"""Catálogo: título, elementos de la interfaz, productos y orden."""
import logging

import pytest

pytestmark = pytest.mark.ui

log = logging.getLogger(__name__)


def test_inventory_title(inventory_page):
    assert inventory_page.driver.title == "Swag Labs"
    assert inventory_page.get_title() == "Products"


def test_inventory_ui_elements(inventory_page):
    assert inventory_page.is_menu_visible(), "No se ve el menú hamburguesa"
    assert inventory_page.is_sort_visible(), "No se ve el filtro de orden"
    assert inventory_page.is_cart_visible(), "No se ve el ícono del carrito"


def test_inventory_has_products(inventory_page):
    products = inventory_page.get_products()
    assert len(products) == 6, f"Se esperaban 6 productos y hay {len(products)}"

    first = products[0]
    log.info("Primer producto: %s - $%.2f", first["name"], first["price"])
    assert first["name"], "El primer producto no tiene nombre"
    assert first["price"] > 0, f"Precio inválido: {first['price']}"


@pytest.mark.parametrize("option, reverse", [
    ("Price (low to high)", False),
    ("Price (high to low)", True),
], ids=["precio-asc", "precio-desc"])
def test_sort_by_price(inventory_page, option, reverse):
    inventory_page.sort_by(option)
    prices = [p["price"] for p in inventory_page.get_products()]

    assert prices == sorted(prices, reverse=reverse), f"Orden incorrecto con '{option}': {prices}"


def test_sort_by_name_z_to_a(inventory_page):
    inventory_page.sort_by("Name (Z to A)")
    names = [p["name"] for p in inventory_page.get_products()]

    assert names == sorted(names, reverse=True), f"Orden incorrecto: {names}"
