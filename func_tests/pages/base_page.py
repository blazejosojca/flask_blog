from selenium import webdriver

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicity_wait(30)
        self.timeout = 30

    def find_element_and_fill(self, *locator, value):
        element  = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def find_element_and_click(self, *locator):
        element = self.driver.find_element(*locator)
        element.click()

