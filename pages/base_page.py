from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Alap Page Object osztály
    Minden oldal-specifikus osztály ebből öröklődik
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """
        Element megkeresése explicit wait-tel
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator):
        """
        Elemre kattintás explicit wait-tel
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """
        Szöveg bevitele mezőbe
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Element szövegének lekérése
        """
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        """
        Elem láthatóságának ellenőrzése
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
    
    def get_current_url(self):
        """
        Aktuális URL lekérése
        """
        return self.driver.current_url