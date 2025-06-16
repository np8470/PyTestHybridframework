from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utilities.SeleniumUtils import SeleniumUtils

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.utils = SeleniumUtils(self.driver)

    # Locators
    FIRST_NAME = (By.ID, "vfb-5")
    LAST_NAME = (By.ID, "vfb-7")
    EMAIL = (By.ID, "vfb-14")
    PHONE = (By.ID, "vfb-19")
    GENDER_MALE = (By.ID, "vfb-31-1")
    GENDER_FEMALE = (By.ID, "vfb-31-2")
    ADDRESS = (By.ID, "vfb-13-address")
    COUNTRY = (By.ID, "vfb-13-country")
    CITY = (By.ID, "vfb-13-city")
    STATE = (By.ID, "vfb-13-state")
    POSTAL_CODE = (By.ID, "vfb-13-zip")
    DATE_OF_DEMO = (By.ID, "vfb-18")
    HOUR = (By.ID, "vfb-16-hour")
    MINUTE = (By.ID, "vfb-16-min")
    SELENIUM_COURSE = (By.ID, "vfb-20-0")
    DEVOPS_COURSE = (By.ID, "vfb-20-3")
    COURSE = (By.XPATH, "//label[normalize-space()='Course Interested']//parent::li//input[@type='checkbox']")
    QUERY = (By.ID, "vfb-23")
    VERIFICATION_CODE = (By.ID, "vfb-3")
    SUBMIT_BTN = (By.ID, "vfb-4")


    def fill_registration_form_util(self, data):
        self.utils.send_text(self.FIRST_NAME, data["first_name"])
        self.utils.send_text(self.LAST_NAME, data["last_name"])

        # Gender selection
        if data["gender"].lower() == "male":
            self.utils.click_element(self.GENDER_MALE)
        else:
            self.utils.click_element(self.GENDER_FEMALE)

        # Course selection (multiple checkboxes)
        for course in data["course"]:
            if course.lower() == "selenium":
                self.utils.select_checkbox(self.SELENIUM_COURSE, should_select=True)
            elif course.lower() == "devops":
                self.utils.select_checkbox(self.DEVOPS_COURSE, should_select=True)

        self.utils.send_text(self.ADDRESS, data["address"])
        self.utils.send_text(self.CITY, data["city"])
        self.utils.send_text(self.STATE, data["state"])
        self.utils.send_text(self.POSTAL_CODE, data["postal_code"])
        self.utils.select_dropdown_by_text(self.COUNTRY, data["country"])

        self.utils.send_text(self.EMAIL, data["email"])
        self.utils.send_text(self.DATE_OF_DEMO, data["date_of_demo"])
        self.utils.select_dropdown_by_text(self.HOUR, data["hour"])
        self.utils.select_dropdown_by_text(self.MINUTE, data["minute"])

        self.utils.send_text(self.PHONE, data["phone"])
        self.utils.send_text(self.QUERY, data["query"])
        self.utils.send_text(self.VERIFICATION_CODE, data["verification_code"])

        self.utils.click_element(self.SUBMIT_BTN)