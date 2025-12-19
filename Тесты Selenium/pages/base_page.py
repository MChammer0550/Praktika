from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
from utils.config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        
    def find_element(self, locator):
        """Найти элемент с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Найти несколько элементов с ожиданием"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.find_element(locator)
        element.click()
        
    def send_keys(self, locator, text):
        """Ввести текст"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        
    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    def is_displayed(self, locator):
        """Проверить, отображается ли элемент"""
        try:
            return self.find_element(locator).is_displayed()
        except TimeoutException:
            return False
    
    def take_screenshot(self, name):
        """Сделать скриншот"""
        timestamp = Config.get_timestamp()
        filename = f"{Config.SCREENSHOT_PATH}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        allure.attach.file(filename, name=name, attachment_type=allure.attachment_type.PNG)
        
    def wait_for_url(self, url_part):
        """Ожидать загрузки URL"""
        self.wait.until(EC.url_contains(url_part))