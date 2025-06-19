from datetime import datetime
import os
import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen

class Test_001_Login:

    base_url = ReadConfig.getApplicationUrl()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()


    def test_homepageTitle(self, setup, logger):
        #logger = logger
        logger.info("*********** Test_001_Login.test_homepageTitle **************")
        self.driver = setup
        self.driver.get(self.base_url)
        logger.info("Successfully launched the application")
        actual_title = self.driver.title
        if actual_title == "nopCommerce demo store. Login":
            assert True
            logger.info("Verify Home Page Title testcase is passed")
        else:
            # This ensures "Screenshots" is relative to the *project root*, not the test file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            screenshots_dir = os.path.join(base_dir, "..", "Screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            # Generate a timestamp in format: YYYYMMDD_HHMMSS
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Create dynamic filename
            filename = f"test_homepageTitle_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, filename)
            success = self.driver.save_screenshot(screenshot_path)
            logger.error("Verify Home Page Title testcase is failed")
            if not success:
                print("Screenshot saving failed")
            assert False

        self.driver.close()

    def test_login(self, setup):
        logger = LogGen().loggen()
        logger.info("*********** Test_001_Login.test_login **************")
        self.driver = setup
        self.driver.get(self.base_url)
        logger.info("Successfully launched the application")
        self.login_page = LoginPage(self.driver)
        logger.info("Enter Username and Password")
        self.login_page.setUserName(self.username)
        self.login_page.setPassword(self.password)
        logger.info("Click Login button")
        self.login_page.clickLogin()
        logger.info("Successfully logged in and Verifying Dashboard page Title")
        actual_title = self.driver.title
        if actual_title == "Dashboard / nopCommerce administration":
            assert True
            logger.info("Verify Dashboard Page Title testcase is passed")
        else:
            logger.error("Verify Dashboard Page Title testcase is failed")
            assert False

        self.driver.close()