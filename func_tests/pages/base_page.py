class BasePage(object):

    def __init__(self, driver, selenium):
        self.driver = driver
        self.url = "http://127.0.0.1:5000/"
        self.title = 'Flask Blog - Home'

    def is_loaded(self):
        return self.driver.title == self.title





