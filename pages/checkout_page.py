"""
Checkout de saucedemo. Son tres pantallas seguidas
(datos del cliente -> resumen -> confirmación), las manejo en una sola clase
porque el flujo es corto.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # Paso 1: datos del cliente
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Paso 2: resumen
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Paso 3: confirmación
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def wait_until_loaded(self):
        self.wait_for_url("/checkout-step-one.html")
        self.find(self.FIRST_NAME_INPUT)
        return self

    def fill_customer_info(self, first_name, last_name, postal_code):
        self.log.info("Datos de checkout: %s %s (%s)", first_name, last_name, postal_code)
        self.write(self.FIRST_NAME_INPUT, first_name)
        self.write(self.LAST_NAME_INPUT, last_name)
        self.write(self.POSTAL_CODE_INPUT, postal_code)

    def get_field_value(self, locator):
        return self.find(locator).get_attribute("value")

    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def get_subtotal(self):
        # Texto tipo "Item total: $29.99"
        self.wait_for_url("/checkout-step-two.html")
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[1])

    def finish(self):
        self.click(self.FINISH_BUTTON)
        self.wait_for_url("/checkout-complete.html")

    def get_confirmation_message(self):
        return self.get_text(self.COMPLETE_HEADER)
