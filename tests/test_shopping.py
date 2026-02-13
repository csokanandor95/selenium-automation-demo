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

    def test_add_multiple_items_to_cart(self):
        """
        Teszt: Több termék hozzáadása a kosárhoz
        """
        # 1. Első termék hozzáadása
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # 2. Második termék hozzáadása
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
        
        # 3. Harmadik termék hozzáadása
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        
        # 4. Ellenőrzés - Kosár számláló = 3
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "3", f"Várt: 3, Kapott: {cart_badge.text}"
        
        print("Több termék kosárba helyezése - PASS")
    
    
    def test_remove_item_from_cart(self):
        """
        Teszt: Termék eltávolítása a kosárból
        """
        # 1. Termék hozzáadása
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # 2. Kosár badge megjelent
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1"
        
        # 3. Termék eltávolítása
        self.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
        
        # 4. Ellenőrzés - Badge eltűnik
        cart_badges = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(cart_badges) == 0, "A kosár badge még mindig látható!"
        
        print("Termék eltávolítása a kosárból - PASS")

    def test_view_cart_page(self):
        """
        Teszt: Kosár oldal megtekintése hozzáadott termékekkel
        """
        # 1. Termék hozzáadása
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # 2. Kosár ikonra kattintás
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # 3. Ellenőrzés - Cart oldalra navigáltunk
        wait = WebDriverWait(self.driver, 10)
        cart_title = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert cart_title.text == "Your Cart"
        
        # 4. Termék megjelenik a kosárban
        cart_item = self.driver.find_element(By.CLASS_NAME, "inventory_item_name")
        assert "Backpack" in cart_item.text
        
        print("Kosár oldal megtekintése - PASS")