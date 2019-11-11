from selenium.webdriver import Chrome, Firefox, Opera
from config import BASEDIR
from config import Config
import os
from app import db
from app.models import User, Post
from func_tests.helpers.func_helpers import load_json

CONFIG_FILE = 'config.json'
UTILS_FILE = 'utils.json'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(THIS_FOLDER, CONFIG_FILE)
UTILS_FILE_PATH = os.path.join(THIS_FOLDER, CONFIG_FILE)
DEFAULT_WAIT_TIME = 10


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'func_test.db')

    def config_browser(self):
        """
        Valid values for browser key
        :return: name of browser from data dict
        """
        data = load_json(CONFIG_FILE_PATH)
        if 'browser' not in data:
            raise Exception('The config file does not contain "browser"')
        elif data['browser'] not in data['supported_browsers']:
            raise Exception(f'"{data["browser"]}" is not supported browser')
        return data['browser']

    def config_wait_time(self):
        """
        Verify and valid values from wait_time key
        :return:
        """
        data = load_json(CONFIG_FILE_PATH)
        return data['wait_time'] if 'wait_time' in data else DEFAULT_WAIT_TIME

    def browser(self):
        config_browser = self.config_browser()
        config_wait_time = self.config_wait_time()
        if config_browser == 'chrome':
            driver = Chrome()
        elif config_browser == 'firefox':
            driver = Firefox()
        elif config_browser == 'opera':
            driver = Opera()
        else:
            raise Exception(f'"{config_browser}" is not a supported browser')

        driver.implicitly_wait(config_wait_time)

        return driver

    def set_up_test_db(self):
        data = load_json(UTILS_FILE)

        db.create_all()

        user = User(username=data["test_user_name"],
                    email=data["test_user_mail"])
        user.set_password(data("test_user_password"))
        post = Post(title='test title', content='test content', author=user)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        admin = User(username=data["test_admin_name"],
                     email=data["test_admin_mail"])
        admin.set_password(data["test_admin_password"])
        admin.is_admin = True

        db.session.add(admin)
        db.session.commit()

    def tear_down_testdb(self):
        db.session.remove()
        db.drop_all()
