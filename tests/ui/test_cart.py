"""Carrito: agregar, agregar varios y quitar."""
import pytest

pytestmark = pytest.mark.ui


def test_add_first_product_to_cart(inventory_page):
    # Arranco confirmando que el carrito está vacío, si no el contador no prueba nada
    assert inventory_page.get_cart_count() == 0, "El carrito no empezó vacío"

    product = inventory_page.add_first_product_to_cart()
    assert inventory_page.get_cart_count() == 1

    cart = inventory_page.go_to_cart()
    assert cart.get_items() == [product], (
        f"En el carrito aparece {cart.get_items()} y se esperaba {[product]}"
    )


def test_add_several_products(inventory_page):
    wanted = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]
    for name in wanted:
        inventory_page.add_product_to_cart(name)

    assert inventory_page.get_cart_count() == len(wanted)

    cart = inventory_page.go_to_cart()
    assert sorted(cart.get_item_names()) == sorted(wanted)


def test_remove_product_from_cart(inventory_page):
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")

    cart = inventory_page.go_to_cart()
    cart.remove_item("Sauce Labs Backpack")

    assert cart.get_item_names() == ["Sauce Labs Bike Light"]
    # El badge está en el header, así que también se ve desde el carrito
    assert inventory_page.get_cart_count() == 1
