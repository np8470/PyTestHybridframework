from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import os
import time

class SeleniumUtils:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def wait_for_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.capture_screenshot("element_not_visible")
            raise Exception(f"Element not visible: {locator}")

    def click_element(self, locator):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            element.click()
        except (ElementClickInterceptedException, TimeoutException):
            # Fallback to JS click
            element = self.driver.find_element(*locator)
            self.scroll_to_element(element)
            self.driver.execute_script("arguments[0].click();", element)

    def send_text(self, locator, text):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.capture_screenshot("send_keys_error")
            raise e

    def select_dropdown_by_text(self, locator, visible_text):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            Select(element).select_by_visible_text(visible_text)
        except Exception as e:
            self.capture_screenshot("dropdown_select_by_visible_text_error")
            raise e

    def select_dropdown_by_value(self, locator, value):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            Select(element).select_by_value(value)
        except Exception as e:
            self.capture_screenshot("dropdown_select_by_value_error")
            raise e

    def select_dropdown_by_index(self, locator, index):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            Select(element).select_by_index(index)
        except Exception as e:
            self.capture_screenshot("dropdown_select_by_index_error")
            raise e

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False

    def select_radio_button(self, locator_list, value):
        for locator in locator_list:
            element = self.driver.find_element(*locator)
            if element.get_attribute("value").lower() == value.lower():
                self.scroll_to_element(element)
                element.click()
                break

    def select_checkbox(self, locator, should_select=True):
        element = self.wait_for_element(locator)
        self.scroll_to_element(element)
        is_selected = element.is_selected()
        if (should_select and not is_selected) or (not should_select and is_selected):
            element.click()

    def get_text(self, locator):
        try:
            element = self.wait_for_element(locator)
            self.scroll_to_element(element)
            return element.text.strip()
        except Exception as e:
            self.capture_screenshot("get_text_error")
            raise e

    def capture_screenshot(self, name_prefix):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = os.path.join(os.getcwd(), "Screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        file_path = os.path.join(screenshot_dir, f"{name_prefix}_{timestamp}.png")
        print("Screenshot saved at", file_path)
        try:
            self.driver.save_screenshot(file_path)
            print(f"✅ Screenshot saved to: {file_path}")
        except Exception as e:
            print(f"❌ Screenshot saving failed: {e}")


