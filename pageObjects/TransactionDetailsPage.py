from selenium.webdriver.common.by import By
from utilities.SeleniumUtils import SeleniumUtils

class TransactionDetailsPage:

    def __init__(self, driver):
        self.driver = driver
        self.utils = SeleniumUtils(self.driver)

    # Locators

    TITLE = (By.XPATH, "//h2[normalize-space()='Transaction Details']")
    SUCCESS_MSG = (By.ID, "messageContainer")

    def verify_title(self, data):
        actual_title = self.utils.get_text(self.TITLE)
        assert actual_title.__eq__(data["title"])

    def verify_success_msg(self, data):
        actual_success_msg = self.utils.get_text(self.SUCCESS_MSG)
        assert actual_success_msg.__contains__(data["success_msg"])

