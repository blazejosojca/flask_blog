from selenium import webdriver

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30

    def find_element_and_fill(self, *locator, value):
        element  = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def find_element_and_click(self, *locator):
        element = self.driver.find_element(*locator)
        element.click()

    def get_title(self, url):
        self.driver.get(url)
        title = self.driver.title
        return title

    def navigate_to_url(self, url):
        self.driver.get(url)


