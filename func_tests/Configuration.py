import json
import unittest
import os
from selenium.webdriver import Chrome, Firefox, Opera
from func_tests.helpers.func_helpers import load_json


CONFIG_FILE = 'config.json'
UTILS_FILE = 'utils.json'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CONF_FILE_PATH = os.path.join(THIS_FOLDER, CONFIG_FILE)
DEFAULT_WAIT_TIME = 10


class TestConfig(object):

    def config_browser(self):
        """
        Valid values for browser key
        :return: name of browser from data dict
        """
        data = load_json(CONF_FILE_PATH)
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
        data = load_json(CONF_FILE_PATH)
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

    @classmethod
    def setUpClass(self):
        self.driver = TestConfig().browser()

    def assert_element_text(self, xpath, expected_text):
        """
        Compare expected text with observed value from web element
        :param xpath: xpath to element with text to be observed
        :param expected_text: text what we expecting to be found
        :return: None
        """
        element = self.driver.find_element_by_xpath(xpath)
        return self.assertEqual(element.text, expected_text,
                                f'Expected message differ from {expected_text}')

    def assert_title(self, url, expected_text):
        """

        :param url:
        :param expected_text:
        :return:
        """
        self.driver.get(url)
        actual_title = self.driver.title
        self.assertEqual(expected_text, actual_title, f'Expected {expected_text} differ from actual driver,')

    @classmethod
    def tearDownClass(self):
        self.driver.close()