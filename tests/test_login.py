import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestLogin:
    """
    Login funkció tesztelése a saucedemo.com oldalon
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Teszt előkészítés és lezárás
        Minden teszt előtt új böngészőt nyit, utána bezárja
        """
        # Chrome driver automatikus telepítése és böngésző indítása
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)  # Implicit várakozás 10 mp
        
        # URL beállítás
        self.base_url = "https://www.saucedemo.com"
        
        yield  # Itt fut le a teszt
        
        # Teardown - böngésző bezárása
        self.driver.quit()
    
    
    def test_successful_login(self):
        """
        Teszt: Sikeres bejelentkezés helyes adatokkal
        """
        # 1. Oldal megnyitása
        self.driver.get(self.base_url)
        
        # 2. Felhasználónév megadása
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")
        
        # 3. Jelszó megadása
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        
        # 4. Login gomb megnyomása
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # 5. Ellenőrzés - Sikeres bejelentkezés után a Products oldal jelenik meg
        wait = WebDriverWait(self.driver, 10)
        products_title = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        
        assert products_title.text == "Products", "Sikertelen bejelentkezés!"
        assert "inventory.html" in self.driver.current_url, "Nem a megfelelő oldalra navigált!"
        
        print("Sikeres bejelentkezés teszt - PASS")
    
    
    def test_login_with_invalid_password(self):
        """
        Teszt: Sikertelen bejelentkezés rossz jelszóval
        """
        # 1. Oldal megnyitása
        self.driver.get(self.base_url)
        
        # 2. Helyes felhasználónév
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")
        
        # 3. ROSSZ jelszó
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("wrong_password")
        
        # 4. Login gomb megnyomása
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # 5. Ellenőrzés - Hibaüzenet megjelenik
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        
        assert "Username and password do not match" in error_message.text
        print("Hibás jelszó teszt - PASS")
    
    
    def test_login_with_locked_user(self):
        """
        Teszt: Zárolt felhasználó bejelentkezési kísérlete
        """
        # 1. Oldal megnyitása
        self.driver.get(self.base_url)
        
        # 2. Zárolt felhasználó
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.send_keys("locked_out_user")
        
        # 3. Jelszó
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        
        # 4. Login gomb megnyomása
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # 5. Ellenőrzés - Zárolt felhasználó hibaüzenet
        wait = WebDriverWait(self.driver, 10)
        error_message = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        
        assert "Sorry, this user has been locked out" in error_message.text
        print("Zárolt felhasználó teszt - PASS")