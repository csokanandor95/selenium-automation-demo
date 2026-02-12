import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestShopping:
    """
    Vásárlási folyamat (shopping cart) tesztelése
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Teszt előkészítés - bejelentkezés minden teszt előtt
        """
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        
        self.base_url = "https://www.saucedemo.com"
        
        # Automatikus bejelentkezés minden teszt előtt
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Várjuk meg, hogy betöltődjön a Products oldal
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        yield
        
        self.driver.quit()
    
    
    def test_add_single_item_to_cart(self):
        """
        Teszt: Egyetlen termék hozzáadása a kosárhoz
        """
        # 1. Első termék "Add to cart" gombjának megkeresése
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-backpack"
        )
        add_to_cart_button.click()
        
        # 2. Ellenőrzés - Shopping cart badge-en megjelenik az "1"
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1", "A kosár számláló nem 1!"
        
        # 3. Gomb szövege "Remove"-ra változik
        remove_button = self.driver.find_element(
            By.ID, "remove-sauce-labs-backpack"
        )
        assert remove_button.text == "Remove", "A gomb nem változott Remove-ra!"
        
        print("Egyetlen termék kosárba helyezése - PASS")