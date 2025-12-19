import time
import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def generate_random_string(length=10):
    """Сгенерировать случайную строку"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def wait_for_element(driver, locator, timeout=10):
    """Ожидать появления элемента"""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located(locator))

def wait_for_element_clickable(driver, locator, timeout=10):
    """Ожидать, пока элемент станет кликабельным"""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable(locator))

def is_logged_in(driver):
    """Проверить, вошел ли пользователь"""
    try:
        # Проверяем наличие элементов, которые видны только после входа
        wait_for_element(driver, (By.CSS_SELECTOR, ".chat-container"), timeout=3)
        return True
    except:
        return False

def take_screenshot(driver, test_name):
    """Сделать скриншот"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename