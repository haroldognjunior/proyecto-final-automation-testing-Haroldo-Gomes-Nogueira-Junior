"""
Página base: todo lo que comparten las páginas (esperas, clicks, escribir texto).

Cada página del sitio hereda de esta clase, así las esperas explícitas
y el logging quedan en un solo lugar.
"""
import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.log = logging.getLogger(self.__class__.__name__)

    def open_url(self, url):
        self.log.info("Abriendo %s", url)
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def write(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        # find_elements no lanza excepción si no encuentra nada
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    def wait_for_url(self, fragment):
        self.wait.until(EC.url_contains(fragment))
