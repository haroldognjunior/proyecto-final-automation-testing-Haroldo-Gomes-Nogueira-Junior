"""Flujo completo de compra, con datos de datos/checkout_data.json."""
import pytest

from utils.helpers import read_json

pytestmark = pytest.mark.ui

CHECKOUT_DATA = read_json("checkout_data.json")


@pytest.mark.parametrize("customer", CHECKOUT_DATA["valid_customers"], ids=lambda c: c["case_id"])
def test_complete_purchase(inventory_page, customer):
    all_products = {p["name"]: p["price"] for p in inventory_page.get_products()}
    for name in customer["products"]:
        inventory_page.add_product_to_cart(name)

    checkout = inventory_page.go_to_cart().go_to_checkout()
    checkout.fill_customer_info(customer["first_name"], customer["last_name"], customer["postal_code"])
    checkout.continue_to_overview()

    # El subtotal tiene que ser la suma de los precios del inventario.
    # round() porque sumar floats da cosas como 33.970000000000006
    expected_subtotal = round(sum(all_products[name] for name in customer["products"]), 2)
    subtotal = checkout.get_subtotal()
    assert subtotal == expected_subtotal, f"Subtotal {subtotal}, esperado {expected_subtotal}"

    checkout.finish()
    assert checkout.get_confirmation_message() == "Thank you for your order!"


@pytest.mark.parametrize("data", CHECKOUT_DATA["missing_fields"], ids=lambda d: d["case_id"])
def test_checkout_required_fields(inventory_page, data):
    inventory_page.add_first_product_to_cart()
    checkout = inventory_page.go_to_cart().go_to_checkout()

    checkout.fill_customer_info(data["first_name"], data["last_name"], data["postal_code"])
    checkout.continue_to_overview()

    error = checkout.get_error_message()
    assert error == data["expected_message"], f"Mensaje inesperado: '{error}'"
    assert "checkout-step-one" in checkout.driver.current_url, "No debería avanzar al resumen"
