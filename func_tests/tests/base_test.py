__author__ = "blazos"

import os
from unittest import TestCase
from datetime import datetime

from app import create_app
from func_tests.test_config import TestConfig


class BaseTest(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app


    @classmethod
    def setUpClass(self):
        self.driver = TestConfig.BROWSER
        print("Run started at:" + str(datetime.utcnow()))

        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

    @classmethod
    def tearDownClass(self):
        self.driver = TestConfig.BROWSER
        if (self.driver!=None):
            print("Test enviroment destroyed.")
            print("Run completed at: " + str(datetime.utcnow()))
            self.driver.close()
            self.driver.quit()
