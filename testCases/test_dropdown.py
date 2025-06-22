import json
import pytest
from pageObjects.DropdownPage import DropdownPage

# load test data from JSON
def load_dropdown_test_data():
     with open("testData/dropdown.json") as f:
         return json.load(f)

class TestDropdown:

    @pytest.mark.system
    @pytest.mark.parametrize("dropdown_data", load_dropdown_test_data())
    def test_dropdown(self, setup, dropdown_data, logger):
        driver = setup
        driver.get("https://vinothqaacademy.com/drop-down/")

        dropdown_page = DropdownPage(driver)
        dropdown_page.select_simple_dropdown(dropdown_data)
        dropdown_page.select_dynamic_dropdown(dropdown_data)
        dropdown_page.select_multiple_dropdown(dropdown_data)


