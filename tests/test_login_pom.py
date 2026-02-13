import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


class TestLoginPOM:
    """
    Login tesztek Page Object Model használatával
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Browser setup és teardown
        """
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        
        # Page Objects inicializálása
        self.login_page = LoginPage(self.driver)
        self.products_page = ProductsPage(self.driver)
        
        yield
        
        self.driver.quit()
    
    
    def test_successful_login_pom(self):
        """
        Teszt: Sikeres bejelentkezés - POM verzió
        """
        # Login oldal megnyitása
        self.login_page.open()
        
        # Bejelentkezés
        self.login_page.login("standard_user", "secret_sauce")
        
        # Ellenőrzés
        assert self.products_page.is_on_products_page(), "Nem sikerült bejelentkezni!"
        assert "inventory.html" in self.products_page.get_current_url()
        
        print("POM Sikeres login - PASS")
    
    
    def test_invalid_password_pom(self):
        """
        Teszt: Sikertelen login rossz jelszóval - POM verzió
        """
        # Login oldal megnyitása
        self.login_page.open()
        
        # Hibás adatokkal próbálkozás
        self.login_page.login("standard_user", "wrong_password")
        
        # Ellenőrzés
        assert self.login_page.is_error_displayed(), "Hibaüzenet nem jelent meg!"
        error_text = self.login_page.get_error_message()
        assert "Username and password do not match" in error_text
        
        print("POM Hibás jelszó - PASS")
    
    
    def test_locked_user_pom(self):
        """
        Teszt: Zárolt felhasználó - POM verzió
        """
        # Login oldal megnyitása
        self.login_page.open()
        
        # Zárolt felhasználóval próbálkozás
        self.login_page.login("locked_out_user", "secret_sauce")
        
        # Ellenőrzés
        assert self.login_page.is_error_displayed(), "Hibaüzenet nem jelent meg!"
        error_text = self.login_page.get_error_message()
        assert "locked out" in error_text.lower()
        
        print("POM Zárolt felhasználó - PASS")
    
    
    def test_empty_credentials_pom(self):
        """
        Teszt: Üres mezőkkel való login próbálkozás - POM verzió
        """
        # Login oldal megnyitása
        self.login_page.open()
        
        # Üres adatokkal login
        self.login_page.click_login()
        
        # Ellenőrzés
        assert self.login_page.is_error_displayed(), "Hibaüzenet nem jelent meg!"
        error_text = self.login_page.get_error_message()
        assert "Username is required" in error_text
        
        print("POM Üres mezők - PASS")