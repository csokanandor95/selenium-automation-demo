import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


class TestShoppingPOM:
    """
    Shopping tesztek Page Object Model használatával
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Browser setup - automatikus bejelentkezéssel
        """

        # Jelszó figyelmeztető letiltása
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
        })

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        
        # Page Objects
        self.login_page = LoginPage(self.driver)
        self.products_page = ProductsPage(self.driver)
        
        # Automatikus bejelentkezés minden teszt előtt
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")
        
        # Várjuk meg a products oldal betöltését
        assert self.products_page.is_on_products_page()
        
        yield
        
        self.driver.quit()
    
    
    def test_add_single_item_pom(self):
        """
        Teszt: Egyetlen termék kosárba helyezése - POM verzió
        """
        # Termék hozzáadása
        self.products_page.add_backpack_to_cart()
        
        # Ellenőrzés - Badge = 1
        assert self.products_page.get_cart_badge_count() == "1"
        
        # Remove gomb megjelenik
        assert self.products_page.is_remove_button_visible()
        
        print("POM Single item - PASS")
    
    
    def test_add_multiple_items_pom(self):
        """
        Teszt: Több termék kosárba helyezése - POM verzió
        """
        # 3 termék hozzáadása
        self.products_page.add_backpack_to_cart()
        self.products_page.add_bike_light_to_cart()
        self.products_page.add_tshirt_to_cart()
        
        # Ellenőrzés - Badge = 3
        assert self.products_page.get_cart_badge_count() == "3"
        
        print("POM Multiple items - PASS")
    
    
    def test_cart_badge_updates_pom(self):
        """
        Teszt: Kosár badge dinamikus frissülése
        """
        # Kezdetben nincs badge
        assert self.products_page.get_cart_badge_count() == "0"
        
        # 1 termék hozzáadása
        self.products_page.add_backpack_to_cart()
        assert self.products_page.get_cart_badge_count() == "1"
        
        # 2. termék hozzáadása
        self.products_page.add_bike_light_to_cart()
        assert self.products_page.get_cart_badge_count() == "2"

        # 3. termék hozzáadása
        self.products_page.add_tshirt_to_cart()
        assert self.products_page.get_cart_badge_count() == "3"

        print("POM Badge update - PASS")