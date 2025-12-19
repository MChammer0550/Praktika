import pytest
import allure
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from data.test_data import TestData
from utils.config import Config
from utils.helpers import is_logged_in

@allure.feature("Авторизация пользователя")
@allure.story("Пользователь может войти в систему")
class TestLogin:
    
    @allure.title("Успешный вход с валидными данными")
    def test_successful_login(self, setup):
        """Тест успешного входа"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(self.driver)
            login_page.open()
            
        with allure.step("Ввести валидные учетные данные"):
            login_page.login(Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
            
        with allure.step("Проверить успешный вход"):
            assert is_logged_in(self.driver)
            login_page.take_screenshot("successful_login")
    
    @allure.title("Вход с неверными данными")
    def test_login_invalid_credentials(self, setup):
        """Тест входа с неверными данными"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(self.driver)
            login_page.open()
            
        with allure.step("Ввести неверные учетные данные"):
            login_page.login(TestData.INVALID_USER["email"], TestData.INVALID_USER["password"])
            
        with allure.step("Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert "invalid" in error_message.lower() or "неверн" in error_message.lower()
            login_page.take_screenshot("login_invalid_credentials")
    
    @allure.title("Вход администратора")
    def test_admin_login(self, setup):
        """Тест входа администратора"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(self.driver)
            login_page.open()
            
        with allure.step("Войти как администратор"):
            login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
            
        with allure.step("Проверить успешный вход администратора"):
            assert is_logged_in(self.driver)
            chat_page = ChatPage(self.driver)
            assert chat_page.is_displayed(chat_page.ADMIN_LINK)
            login_page.take_screenshot("admin_login")
    
    @allure.title("Переход на страницу регистрации")
    def test_go_to_registration(self, setup):
        """Тест перехода на страницу регистрации"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(self.driver)
            login_page.open()
            
        with allure.step("Нажать ссылку регистрации"):
            login_page.go_to_register()
            
        with allure.step("Проверить переход на страницу регистрации"):
            assert "Register" in self.driver.current_url
            login_page.take_screenshot("go_to_registration")