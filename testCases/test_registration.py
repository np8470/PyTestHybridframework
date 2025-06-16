import pytest
import json
from pageObjects.RegistrationPage import RegistrationPage
from pageObjects.TransactionDetailsPage import TransactionDetailsPage

#Load test data from JSON
def load_register_test_data():
    with open("testData/registration_data.json") as f:
        return json.load(f)

def load_transaction_test_data():
    with open("testData/transaction_data.json") as f:
        return json.load(f)[0] # use first object if it's a list


@pytest.mark.parametrize("reg_data", load_register_test_data())
def test_fill_registration_form(setup, reg_data, logger):
    driver = setup
    driver.get("https://vinothqaacademy.com/demo-site/")
    reg_page = RegistrationPage(driver)
    reg_page.fill_registration_form_util(reg_data)

    #  verify registration success here

    transaction_data = load_transaction_test_data()  # loaded once per test run

    transaction_page = TransactionDetailsPage(driver)
    transaction_page.verify_title(transaction_data)
    transaction_page.verify_success_msg(transaction_data)
