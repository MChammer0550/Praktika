import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import sys
from pathlib import Path

class Config:
    BASE_URL = "https://localhost:7227"
    BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    SCREENSHOT_PATH = "screenshots"
    
    # Пути к драйверам
    CHROMEDRIVER_PATH = r"C:\WebDrivers\chromedriver.exe"
    GECKODRIVER_PATH = r"C:\WebDrivers\geckodriver.exe"

def get_chrome_driver():
    """Создать Chrome драйвер без webdriver-manager"""
    chrome_options = Options()
    
    # Настройки для localhost HTTPS
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    if Config.HEADLESS:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    # Принимаем небезопасные сертификаты
    chrome_options.set_capability('acceptInsecureCerts', True)
    
    # Пробуем разные варианты
    driver = None
    
    # Вариант 1: Проверяем указанный путь
    if os.path.exists(Config.CHROMEDRIVER_PATH):
        print(f"Using ChromeDriver from: {Config.CHROMEDRIVER_PATH}")
        service = Service(Config.CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Вариант 2: Проверяем в PATH
    elif driver is None:
        try:
            print("Trying ChromeDriver from PATH...")
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"ChromeDriver not in PATH: {e}")
    
    # Вариант 3: Проверяем в папке проекта
    elif driver is None:
        project_driver = Path("chromedriver.exe")
        if project_driver.exists():
            print(f"Using ChromeDriver from project folder")
            service = Service(str(project_driver))
            driver = webdriver.Chrome(service=service, options=chrome_options)
    
    if driver is None:
        raise Exception(
            "ChromeDriver not found!\n"
            "Please download from: https://chromedriver.chromium.org/\n"
            "And place in: C:\\WebDrivers\\ or project folder"
        )
    
    return driver

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера"""
    browser = Config.BROWSER.lower()
    
    if browser == "chrome":
        driver_instance = get_chrome_driver()
    elif browser == "firefox":
        # Аналогично для Firefox
        firefox_options = FirefoxOptions()
        firefox_options.set_preference('accept_insecure_certs', True)
        if Config.HEADLESS:
            firefox_options.add_argument("--headless")
        driver_instance = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Browser {browser} not supported")
    
    # Настройки драйвера
    driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
    driver_instance.maximize_window()
    
    # Создаем папку для скриншотов
    os.makedirs(Config.SCREENSHOT_PATH, exist_ok=True)
    
    yield driver_instance
    
    # Закрытие после теста
    driver_instance.quit()

@pytest.fixture(scope="function")
def setup(driver):
    """Базовая фикстура"""
    yield driver