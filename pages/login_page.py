from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Login oldal Page Object
    """
    
    # Locators - Elemek azonosítói
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com"
    
    def open(self):
        """
        Login oldal megnyitása
        """
        self.driver.get(self.url)
    
    def enter_username(self, username):
        """
        Felhasználónév megadása
        """
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """
        Jelszó megadása
        """
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """
        Login gomb megnyomása
        """
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """
        Teljes login folyamat egy metódusban
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self):
        """
        Hibaüzenet lekérése
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        """
        Hibaüzenet megjelenésének ellenőrzése
        """
        return self.is_element_visible(self.ERROR_MESSAGE)