from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class RegisterPage(BasePage):
    # Локаторы
    FIRST_NAME_INPUT = (By.ID, "Input_FirstName")
    LAST_NAME_INPUT = (By.ID, "Input_LastName")
    EMAIL_INPUT = (By.ID, "Input_Email")
    PASSWORD_INPUT = (By.ID, "Input_Password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "Input_ConfirmPassword")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK = (By.LINK_TEXT, "Login here")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".text-danger")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/Account/Register"
        
    def open(self):
        """Открыть страницу регистрации"""
        self.driver.get(f"{self.driver.current_url.split('/')[0]}//{self.driver.current_url.split('/')[2]}{self.url}")
        
    def register(self, first_name, last_name, email, password):
        """Зарегистрировать нового пользователя"""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.REGISTER_BUTTON)
        
    def get_error_messages(self):
        """Получить все сообщения об ошибках"""
        errors = []
        if self.is_displayed(self.ERROR_MESSAGES):
            elements = self.find_elements(self.ERROR_MESSAGES)
            errors = [elem.text for elem in elements]
        return errors