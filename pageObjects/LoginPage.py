from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:

    textbox_username_id="Email"
    textbox_password_id="Password"
    button_login_xpath="//button[normalize-space(.)='Log in']"
    link_logout_linktext="Logout"
    link_logout_xpath="//a[normalize-space(.)='Logout']"
    dashboard_xpath="//h1[normalize-space()='Dashboard']"

    def __init__(self, driver):
        self.driver = driver

    def setUserName(self, username):
        #self.driver.find_element_by_id(self.textbox_username_id).clear()
        #self.driver.find_element_by_id(self.textbox_username_id).send_keys(username)
         self.driver.find_element(By.ID,self.textbox_username_id).clear()
         self.driver.find_element(By.ID,self.textbox_username_id).send_keys(username)
    def setPassword(self, password):
        self.driver.find_element(By.ID,self.textbox_password_id).clear()
        self.driver.find_element(By.ID,self.textbox_password_id).send_keys(password)

    def clickLogin(self):
        self.driver.find_element(By.XPATH,self.button_login_xpath).click()
        #WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(self.driver.find_element(By.XPATH,self.dashboard_xpath)))

    def clickLogout(self):
        #self.driver.find_element(By.LINK_TEXT,self.link_logout_linktext).click()
         self.driver.find_element(By.XPATH,self.link_logout_xpath).click()