__author__ = "blazos"

from .base_test import BaseTest
from func_tests.pages.main_page import MainPage
from func_tests.pages.base_page import BasePage
from func_tests.locators.login_locators import LoginPageLocators


class LoginTest(BaseTest):
    """
    Navigate to login page.
    Login valid credentials.
    Redirect to account page.
    Verify the user name with displayed in top bar.
    """
    def test_navigate_to_login_page(self):
        self.driver.get(MainPage.MAIN_PAGE_URL)