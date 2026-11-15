from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):

    PAGE_TITLE = (By.CSS_SELECTOR, "span.title")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.TAG_NAME, "button")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def wait_until_loaded(self):
        self.wait_for_url("/cart.html")
        self.find(self.PAGE_TITLE)
        return self

    def get_items(self):
        # find_elements y no find_all: el carrito puede estar vacío
        items = []
        for row in self.driver.find_elements(*self.CART_ITEM):
            items.append({
                "name": row.find_element(*self.ITEM_NAME).text,
                "price": float(row.find_element(*self.ITEM_PRICE).text.replace("$", "")),
            })
        return items

    def get_item_names(self):
        return [item["name"] for item in self.get_items()]

    def remove_item(self, product_name):
        for row in self.driver.find_elements(*self.CART_ITEM):
            if row.find_element(*self.ITEM_NAME).text == product_name:
                row.find_element(*self.REMOVE_BUTTON).click()
                self.log.info("Quitado del carrito: %s", product_name)
                return
        raise ValueError(f"'{product_name}' no está en el carrito")

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver).wait_until_loaded()
