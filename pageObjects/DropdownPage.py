from selenium.webdriver.common.by import By
from utilities.SeleniumUtils import SeleniumUtils

class DropdownPage:

    def __init__(self, driver):
        self.driver = driver
        self.utils = SeleniumUtils(self.driver)

    # Locators

    SIMPLE_DROPDWON = (By.ID, "simpleDropdown")
    DYNAMIC_DROPDWON= (By.ID, "FromAccount")
    MULTIPLE_SELECT = (By.NAME, "programming")

    def select_simple_dropdown(self, data):
        self.utils.select_dropdown_by_value(self.SIMPLE_DROPDWON, data["city"])

    def select_dynamic_dropdown(self, data):
        self.utils.select_dropdown_by_index(self.DYNAMIC_DROPDWON, data["account"])

    def select_multiple_dropdown(self, data):
        for language in data["programming languages"]:
            self.utils.select_dropdown_by_text(self.MULTIPLE_SELECT, language)
