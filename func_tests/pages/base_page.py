from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from func_tests.helpers.func_helpers import load_json

class BasePage(object):

    base_url = 'http://127.0.0.1:5000/'

    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)


    def find_element_and_fill(self, *locator, value):
        element  = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def find_element_and_click(self, *locator):
        element = self.driver.find_element(*locator)
        element.click()

    def get_page_title(self, url):
        self.driver.get(url)
        title = self.driver.title
        return title

    def navigate_to_url(self, url):
        self.driver.get(url)

    def scroll_find_and_wait_for_element(self, xpath, x_location, y_location):
        self.driver.execute_script("window.scrollTo('{0}', '{1}')".format(x_location, y_location))
        wait = WebDriverWait(self.driver, 2)
        element = wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        return element


