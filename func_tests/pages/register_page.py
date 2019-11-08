from selenium.webdriver.common.by import By
from func_tests.pages.base_page import BasePage

class RegisterPage(BasePage):
    _register_page_title = "Flask Blog = Register"
    _register_url = BasePage._base_url + '/*'
