import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
import os


class TestShoppingPOM:
    """
    Shopping tesztek Page Object Model használatával
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Browser setup - automatikus bejelentkezéssel
        CI környezetben headless módban fut
        """
        # Chrome options konfigurálása
        chrome_options = webdriver.ChromeOptions()
        
        # Jelszó figyelmeztető letiltása
        chrome_options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        })
        
        # CI környezet (GitHub Actions) észlelése
        if os.getenv('CI'):
            print("CI environment detected - running in headless mode")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox') # Sandbox biztonsági funkció letiltása: Linux container környezetben szükséges
            chrome_options.add_argument('--disable-dev-shm-usage') # Elkerüli a /dev/shm memória problémákat Docker/CI környezetben
            chrome_options.add_argument('--disable-gpu') # GPU gyorsítás kikapcsolása, Headless módban nem kell, elkerüli a crash-eket
            chrome_options.add_argument('--window-size=1920,1080') # Virtuális ablak méret beállítása, hogy ugyanúgy jelenjenek meg az elemek mint normál módban
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
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

    def test_checkout_pom(self):
        """
        Teszt lépések: 
            Add 1 item to cart
            Item appears in cart
            Click cart
            'Your cart' page loads and checkout button appears
            Click checkout
            'Checkout: Your Information' page loads
            Fill in First Name, Last name, Zip/Postal code then click Continue (negative test to make here)
            'Checkout: Overview' page loads
            Click finish
        """
        # Termék hozzáadása
        self.products_page.add_backpack_to_cart()

        # Ellenőrzés - Badge = 1
        assert self.products_page.get_cart_badge_count() == "1"

        # Kosárra kattintás
        self.products_page.click_cart()

        # Ellenőrzés - checkout gomb látszik-e
        self.products_page.is_checkout_button_visible()

        # Checkout gombra kattintás
        self.products_page.click_checkout()

        # Ellenőrzés - Checkout: Your Information oldalon vagyunk-e
        assert self.products_page.get_page_title() == "Checkout: Your Information"

        # Beírni az adatokat a checkouthoz
        self.products_page.enter_checkout_credentials()

        # Ellenőrzés - continue gomb látszik-e
        self.products_page.is_continue_button_visible()

        # Continue gombra kattintás
        self.products_page.click_continue()

        # Ellenőrzés - Checkout: Your Information oldalon vagyunk-e
        assert self.products_page.get_page_title() == "Checkout: Overview"



