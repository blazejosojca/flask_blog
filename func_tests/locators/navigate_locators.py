from selenium.webdriver.common.by import By


class NavigateLocators(object):
    CSS_HOME_NAVBAR_LINK = By.CSS_SELECTOR("div.navbar-nav:nth-child(1) > a:nth-child(1)")

    CSS_ABOUT_NAVBAR_LINK = By.CSS_SELECTOR("div.navbar-nav:nth-child(1) > a:nth-child(2)")

    CSS_LOGIN_NAVBAR_LINK = By.CSS_SELECTOR("div.navbar-nav:nth-child(2) > a:nth-child(1)")

    CSS_REGISTER_NAVBAR_LINK = By.CSS_SELECTOR("div.navbar-nav:nth-child(2) > a:nth-child(2)")

    CSS_FLASK_BLOG_TITLE = By.CSS_SELECTOR(".display-3 > a:nth-child(1)")
