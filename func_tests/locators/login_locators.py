from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    CSS_LOGIN_IN_STRING = (By.CSS_SELECTOR(".border-bottom"))

    CSS_EMAIL_FORM = (By.CSS_SELECTOR("#email"))

    CSS_PASSWORD_FORM = (By.CSS_SELECTOR("#password"))

    CSS_SUBMIT_BUTTON = (By.CSS_SELECTOR("#submit"))

    CSS_REMEMBER_ME_CHECKBOX= (By.CSS_SELECTOR("#remember"))

    CSS_RESET_PASSWORD_LINK= (By.CSS_SELECTOR("small.text-muted:nth-child(4) > a:nth-child(1)"))

    CSS_REGISTER_PAGE_LINK = (By.CSS_SELECTOR("a.ml-2"))

