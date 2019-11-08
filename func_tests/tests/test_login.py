__author__ = "blazos"

from .base_test import BaseTest
from func_tests.pages.home_page import HomePage
from func_tests.locators.home_page_locators import MainPageLocators
from func_tests.locators.login_locators import LoginLocators

class LoginTest(BaseTest):
    """
    Navigate to login page.
    Login valid credentials.
    Redirect to account page.
    Verify the user name with displayed in top bar.
    """
    def test_login_page(self):
        browser = self.driver
        HomePage(browser, HomePage.base_url)
        nav_link = browser.find_element_by_xpath(MainPageLocators.NAV_LINK_LOGIN)
        nav_link.click()
        browser.implicitly_wait(30)
        email_field = browser.find_element_by_xpath(LoginLocators.XPATH_EMAIL_FIELD)
        email_field.clear()
        email_field.send_keys()

        page_title = browser.title

        self.assertEqual(page_title, 'Flask Blog - Login')




