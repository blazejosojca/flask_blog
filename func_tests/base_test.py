from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from app import create_app
from config import Config

create_app(Config)


driver = webdriver.Firefox()


url = "http://127.0.0.1:5000/bp"
css_login = "div.navbar-nav:nth-child(2) > a:nth-child(1)"
css_email_login_input = "#email"
css_password_input = "#password"
css_signin = "#submit"
driver.get(url)
driver.implicitly_wait(3)
driver.find_element_by_css_selector(css_login).click()
driver.implicitly_wait(3)
email_login_field = driver.find_element_by_css_selector(css_email_login_input)
driver.implicitly_wait(3)

email_login_field.send_keys("joe1@mail.com")
password_login_field = driver.find_element_by_css_selector(css_password_input)
driver.implicitly_wait(3)
password_login_field.send_keys("xxxxxxx")
driver.implicitly_wait(3)

sign_in_button = driver.find_element_by_css_selector(css_signin)
sign_in_button.click()




