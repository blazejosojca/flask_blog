from selenium.webdriver.common.by import By
from func_tests.pages.base_page import BasePage

class HomePage(BasePage):
    home_page_title = "Flask Blog = Home"
    home_url = BasePage.base_url + '/home'


