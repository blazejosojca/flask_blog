
from selenium import webdriver
from config import BASEDIR
from app import create_app
from config import Config
import os


TEST_USER_NAME = 'automation_test_user'
TEST_USER_EMAIL = 'automation_test@mail.com'
TEST_PASSWORD = 'automation_password'
TEST_ADMIN_NAME = 'automation_test_admin'
TEST_ADMIN_MAIL = 'automation_admin@mail.com'
TEST_ADMIN_PASSWORD = 'automation_admin123'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'func_test.db')
    BROWSER = webdriver.Firefox()
