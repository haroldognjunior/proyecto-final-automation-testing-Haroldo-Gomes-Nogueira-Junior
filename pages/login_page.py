import os

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

# Se puede apuntar a otro entorno con la variable BASE_URL
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.open_url(BASE_URL)
        self.find(self.USERNAME_INPUT)
        return self

    def login(self, username, password):
        self.log.info("Login con usuario '%s'", username)
        self.write(self.USERNAME_INPUT, username)
        self.write(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
