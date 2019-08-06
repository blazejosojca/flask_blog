from selenium.webdriver.common.by import By
from func_tests.pages.base_page import BasePage

from func_tests.pages.main_page import MainPage

class LoginPage(BasePage):

    LOGIN_URL = MainPage.MAIN_PAGE_URL + '/auth/login'

    def test_login_page_title(self, url):
        self.get_title(url)

    def set_email(self):
        pass

    def set_password(self):
        pass

    def click_button(self):
        pass

    def click_remember_me(self):
        pass

    def click_reset_password(self):
        pass

    def click_redirect_to_register(self):
        pass

