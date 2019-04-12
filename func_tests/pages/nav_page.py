from func_tests.pages.base_page import BasePage

class NavPage(BasePage):

    def open(self):
        self.driver.get(self.url)