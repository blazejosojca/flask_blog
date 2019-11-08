from selenium.webdriver.common.by import By
from func_tests.pages.base_page import BasePage

from func_tests.pages.base_page import BasePage
from func_tests.locators.login_locators import *
from func_tests import Configuration
from func_tests.locators.login_locators import LoginLocators
class LoginPage(BasePage):

    login_url = BasePage.base_url + '/auth/login'
    login_title = 'Flask Blog - Login'
    header_text = 'Log In!'
    failed_message = 'Authentication failed.'


    def user_login(self, email, password):
        email_xpath = LoginPageLocators.XPATH_LOGIN_EMAIL_FIELD
        password_xpath = LoginPageLocators.XPATH_LOGIN_PASSWORD_FIELD
        sign_in_xpath = LoginPageLocators.XPATH_LOGIN_SIGNIN_BTN
        self.find_and_fill_by_xpath(email_xpath, email)
        self.find_and_fill_by_xpath(password_xpath, password)
        self.find_and_click_by_xpath(sign_in_xpath)

    def login_with_valid_credentials(self):
        email = self.CORRECT_EMAIL
        password = self.CORRECT_PASSWORD
        self.user_login(email, password)

    def login_with_invalid_credentials(self):
        email = self.INCORRECT_EMAIL
        password = self.INCORRECT_PASSWORD
        self.user_login(email, password)

    def test_login_page_title(self, url):
        self.get_page_title(url)

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

