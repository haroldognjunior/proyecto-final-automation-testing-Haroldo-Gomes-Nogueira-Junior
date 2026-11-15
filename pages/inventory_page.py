from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):

    APP_LOGO = (By.CLASS_NAME, "app_logo")
    PAGE_TITLE = (By.CSS_SELECTOR, "span.title")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_CARD = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img.inventory_item_img")
    PRODUCT_BUTTON = (By.TAG_NAME, "button")  # "Add to cart" o "Remove"
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def wait_until_loaded(self):
        self.wait_for_url("/inventory.html")
        self.find(self.PAGE_TITLE)
        return self

    def get_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_logo_text(self):
        return self.get_text(self.APP_LOGO)

    def get_products(self):
        """Lista de productos como diccionarios: {'name': ..., 'price': ...}."""
        products = []
        for card in self.find_all(self.PRODUCT_CARD):
            name = card.find_element(*self.PRODUCT_NAME).text
            price_text = card.find_element(*self.PRODUCT_PRICE).text  # ej: "$29.99"
            products.append({"name": name, "price": float(price_text.replace("$", ""))})
        return products

    def get_image_sources(self):
        return [img.get_attribute("src") for img in self.find_all(self.PRODUCT_IMAGE)]

    def _find_card_by_name(self, product_name):
        for card in self.find_all(self.PRODUCT_CARD):
            if card.find_element(*self.PRODUCT_NAME).text == product_name:
                return card
        raise ValueError(f"No existe el producto '{product_name}' en el inventario")

    def add_product_to_cart(self, product_name):
        card = self._find_card_by_name(product_name)
        card.find_element(*self.PRODUCT_BUTTON).click()
        self.log.info("Agregado al carrito: %s", product_name)

    def add_first_product_to_cart(self):
        first_product = self.get_products()[0]
        self.add_product_to_cart(first_product["name"])
        return first_product

    def get_cart_count(self):
        # Con el carrito vacío el badge no existe
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def sort_by(self, visible_text):
        self.log.info("Ordenando productos por '%s'", visible_text)
        Select(self.find(self.SORT_SELECT)).select_by_visible_text(visible_text)

    def is_menu_visible(self):
        return self.is_visible(self.BURGER_MENU)

    def is_sort_visible(self):
        return self.is_visible(self.SORT_SELECT)

    def is_cart_visible(self):
        return self.is_visible(self.CART_LINK)

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver).wait_until_loaded()
