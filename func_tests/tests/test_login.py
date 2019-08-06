__author__ = "blazos"

from .base_test import BaseTest
from func_tests.pages.main_page import MainPage
from func_tests.locators.main_locators import MainPageLocators
from func_tests.pages.base_page import BasePage
from func_tests.pages.login_page import LoginPage



class LoginTest(BaseTest):
    """
    Navigate to login page.
    Login valid credentials.
    Redirect to account page.
    Verify the user name with displayed in top bar.
    """
    def test_login_page(self):
        browser = self.driver
        main_page = MainPage(browser)
        main_page.navigate_to_url(MainPage.MAIN_PAGE_URL)
        element = browser.find_element_by_xpath(MainPageLocators.NAV_LINK_LOGIN)
        element.click()
        browser.implicitly_wait(15)
        page_title = browser.title

        self.assertEqual(page_title, 'Flask Blog - Login')




