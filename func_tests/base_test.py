
__author__ = "Mega Author"

import os
from unittest import TestCase
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import BASEDIR
from app import create_app
from config import Config


TEST_USER_NAME = 'test_user'
TEST_USER_EMAIL = 'test@mail.com'
TEST_PASSWORD = 'password'
TEST_ADMIN_NAME = 'test_admin'
TEST_ADMIN_MAIL = 'admin@mail.com'
TEST_ADMIN_PASSWORD = 'admin123'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'func_test.db')


class BaseTest(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app


    def setUp(self):
        self.driver = webdriver.Firefox()
        print("Run started at:" + str(datetime.utcnow()))

        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

    def tearDown(self):
        if (self.driver!=None):
            print("Test enviroment destroyed.")
            print("Run completed at: " + str(datetime.utcnow()))
            self.driver.close()
            self.driver.quit()

#
#
#
# driver = webdriver.Firefox()
#
#
# url = "http://127.0.0.1:5000/"
# css_login = "div.navbar-nav:nth-child(2) > a:nth-child(1)"
# css_email_login_input = "#email"
# css_password_input = "#password"
# css_signin = "#submit"
# driver.get(url)
# driver.implicitly_wait(3)
# driver.find_element_by_css_selector(css_login).click()
# driver.implicitly_wait(3)
# email_login_field = driver.find_element_by_css_selector(css_email_login_input)
# driver.implicitly_wait(3)
#
# email_login_field.send_keys("joe1@mail.com")
# password_login_field = driver.find_element_by_css_selector(css_password_input)
# driver.implicitly_wait(3)
# password_login_field.send_keys("xxxxxxx")
# driver.implicitly_wait(3)
#
# sign_in_button = driver.find_element_by_css_selector(css_signin)
# sign_in_button.click()




