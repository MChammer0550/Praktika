from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # Локаторы
    EMAIL_INPUT = (By.ID, "Input_Email")
    PASSWORD_INPUT = (By.ID, "Input_Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_LINK = (By.LINK_TEXT, "Register here")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/Account/Login"
        
    def open(self):
        """Открыть страницу логина"""
        self.driver.get(f"{self.driver.current_url.split('/')[0]}//{self.driver.current_url.split('/')[2]}{self.url}")
        
    def login(self, email, password):
        """Выполнить вход"""
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        
    def go_to_register(self):
        """Перейти на страницу регистрации"""
        self.click(self.REGISTER_LINK)
        
    def get_error_message(self):
        """Получить текст ошибки"""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""