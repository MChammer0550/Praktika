import pytest
import allure
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from data.test_data import TestData
from utils.config import Config

@allure.feature("Регистрация пользователя")
@allure.story("Пользователь может зарегистрироваться в системе")
class TestRegistration:
    
    @allure.title("Успешная регистрация нового пользователя")
    def test_successful_registration(self, setup):
        """Тест успешной регистрации"""
        with allure.step("Открыть страницу регистрации"):
            login_page = LoginPage(self.driver)
            login_page.open()
            login_page.go_to_register()
            
        with allure.step("Заполнить форму регистрации"):
            register_page = RegisterPage(self.driver)
            test_email = TestData.generate_email()
            register_page.register(
                first_name="Test",
                last_name="User",
                email=test_email,
                password=Config.TEST_USER_PASSWORD
            )
            
        with allure.step("Проверить успешную регистрацию"):
            # После регистрации должен быть редирект на главную страницу
            assert "Index" in self.driver.current_url
            register_page.take_screenshot("successful_registration")
    
    @allure.title("Регистрация с существующим email")
    def test_registration_existing_email(self, setup):
        """Тест регистрации с существующим email"""
        with allure.step("Открыть страницу регистрации"):
            login_page = LoginPage(self.driver)
            login_page.open()
            login_page.go_to_register()
            
        with allure.step("Попытаться зарегистрироваться с существующим email"):
            register_page = RegisterPage(self.driver)
            register_page.register(
                first_name="Test",
                last_name="User",
                email=Config.TEST_USER_EMAIL,
                password=Config.TEST_USER_PASSWORD
            )
            
        with allure.step("Проверить наличие ошибки"):
            errors = register_page.get_error_messages()
            assert len(errors) > 0
            assert "already exists" in " ".join(errors).lower() or "уже существует" in " ".join(errors).lower()
            register_page.take_screenshot("registration_existing_email")
    
    @allure.title("Регистрация с невалидными данными")
    @pytest.mark.parametrize("first_name,last_name,email,password", [
        ("", "User", "test@example.com", "Test123!"),  # Пустое имя
        ("Test", "", "test@example.com", "Test123!"),  # Пустая фамилия
        ("Test", "User", "invalid-email", "Test123!"),  # Невалидный email
        ("Test", "User", "test@example.com", "123"),     # Короткий пароль
    ])
    def test_registration_invalid_data(self, setup, first_name, last_name, email, password):
        """Тест регистрации с невалидными данными"""
        with allure.step("Открыть страницу регистрации"):
            login_page = LoginPage(self.driver)
            login_page.open()
            login_page.go_to_register()
            
        with allure.step("Попытаться зарегистрироваться с невалидными данными"):
            register_page = RegisterPage(self.driver)
            register_page.register(first_name, last_name, email, password)
            
        with allure.step("Проверить наличие ошибок валидации"):
            errors = register_page.get_error_messages()
            assert len(errors) > 0
            register_page.take_screenshot(f"registration_invalid_data_{first_name}")