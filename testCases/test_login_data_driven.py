import time
from datetime import datetime
import os
import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import ExcelUtils

class Test_002_Login_DataDriven:

    base_url = ReadConfig.getApplicationUrl()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    testdata_dir = os.path.join(base_dir, "Testdata")
    os.makedirs(testdata_dir, exist_ok=True)

    testdata_path = os.path.join(testdata_dir, "LoginData.xlsx")
    print(f"[DIR] TestData Path: {testdata_path}")


    def test_login(self, setup):
        logger = LogGen().loggen()
        logger.info("*********** Test_002_Login_DataDriven.test_login **************")
        self.driver = setup
        self.driver.get(self.base_url)
        logger.info("Successfully launched the application")
        self.login_page = LoginPage(self.driver)

        self.rows = ExcelUtils.getRowCount(self.testdata_path, 'Sheet1')
        print("Number of rows in Excel: ", self.rows)

        list_status = [] # Empty list variable to store status
        for r in range(2, self.rows+1):
            self.username = ExcelUtils.readData(self.testdata_path, 'Sheet1', r, 1)
            self.password = ExcelUtils.readData(self.testdata_path, 'Sheet1', r, 2)
            self.expected = ExcelUtils.readData(self.testdata_path, 'Sheet1', r, 3)

            self.login_page.setUserName(self.username)
            self.login_page.setPassword(self.password)
            self.login_page.clickLogin()
            time.sleep(5)

            actual_title = self.driver.title
            expected_title = "Dashboard / nopCommerce administration"

            if actual_title == expected_title:
                if self.expected == "Pass":
                    logger.info("Passed....Title match")
                    self.login_page.clickLogout()
                    list_status.append("Pass")
                elif self.expected == "Fail":
                    logger.info("Failed....Title match")
                    self.login_page.clickLogout()
                    list_status.append("Fail")
            elif actual_title != expected_title:
                if self.expected == "Pass":
                    logger.info("Failed....Title does not match")
                    list_status.append("Fail")
                elif self.expected == "Fail":
                    logger.info("Passed....Title does not match")
                    list_status.append("Pass")

        if "Fail" not in list_status:
            logger.info("***** Login Test passed through Data Driven approach *******")
            self.driver.close()
            assert True, "Data Driven approach Passed"
        else:
             logger.info("***** Login Test failed through Data Driven approach *******")
             self.driver.close()
             assert False, "Data Driven approach Failed"

        logger.info("*********** End of Test_002_Login_DataDriven.test_login **************")


