from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """
    Products (inventory) oldal Page Object
    """
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    # Termék gombok
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    ADD_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    ADD_TSHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_title(self):
        """
        Oldal címének lekérése
        """
        return self.get_text(self.PAGE_TITLE)
    
    def is_on_products_page(self):
        """
        Ellenőrzés: Products oldalon vagyunk-e
        """
        return self.is_element_visible(self.INVENTORY_LIST) and \
               self.get_page_title() == "Products"
    
    def add_backpack_to_cart(self):
        """
        Backpack termék kosárba helyezése
        """
        self.click_element(self.ADD_BACKPACK)
    
    def add_bike_light_to_cart(self):
        """
        Bike Light termék kosárba helyezése
        """
        self.click_element(self.ADD_BIKE_LIGHT)
    
    def add_tshirt_to_cart(self):
        """
        T-Shirt termék kosárba helyezése
        """
        self.click_element(self.ADD_TSHIRT)
    
    def get_cart_badge_count(self):
        """
        Kosár badge számának lekérése
        """
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"  # Ha nincs badge, akkor üres a kosár
    
    def click_cart(self):
        """
        Kosár ikonra kattintás
        """
        self.click_element(self.CART_LINK)
    
    def is_remove_button_visible(self):
        """
        Remove gomb láthatóságának ellenőrzése (Backpack termékhez)
        """
        return self.is_element_visible(self.REMOVE_BACKPACK)