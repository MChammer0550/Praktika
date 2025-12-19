import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from data.test_data import TestData
from utils.config import Config

@allure.feature("Обмен сообщениями")
@allure.story("Пользователь может отправлять и получать сообщения")
class TestMessaging:
    
    @pytest.fixture(autouse=True)
    def login(self, setup):
        """Фикстура для входа перед каждым тестом"""
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
        yield
        # Выход после теста
        chat_page = ChatPage(self.driver)
        chat_page.logout()
    
    @allure.title("Отправка сообщения")
    def test_send_message(self):
        """Тест отправки сообщения"""
        with allure.step("Выбрать контакт"):
            chat_page = ChatPage(self.driver)
            contacts_count = chat_page.get_contacts_count()
            
            if contacts_count > 0:
                # Выбираем первый контакт
                chat_page.select_contact("Test")
                assert chat_page.is_displayed(chat_page.MESSAGE_INPUT)
                
                with allure.step("Отправить тестовое сообщение"):
                    test_message = TestData.TEST_MESSAGES[0]
                    chat_page.send_message(test_message)
                    time.sleep(2)  # Ждем отправки
                    
                with allure.step("Проверить отправку сообщения"):
                    last_message = chat_page.get_last_message()
                    assert test_message in last_message
                    chat_page.take_screenshot("send_message")
            else:
                pytest.skip("Нет контактов для тестирования")
    
    @allure.title("Поиск контакта")
    def test_search_contact(self):
        """Тест поиска контакта"""
        with allure.step("Выполнить поиск контакта"):
            chat_page = ChatPage(self.driver)
            initial_count = chat_page.get_contacts_count()
            
            if initial_count > 0:
                chat_page.search_contact("Test")
                time.sleep(1)  # Ждем фильтрации
                
                with allure.step("Проверить результаты поиска"):
                    # После поиска должно отображаться меньше или столько же контактов
                    filtered_count = chat_page.get_contacts_count()
                    assert filtered_count <= initial_count
                    chat_page.take_screenshot("search_contact")
            else:
                pytest.skip("Нет контактов для тестирования")
    
    @allure.title("Отправка нескольких сообщений")
    def test_send_multiple_messages(self):
        """Тест отправки нескольких сообщений"""
        with allure.step("Выбрать контакт"):
            chat_page = ChatPage(self.driver)
            contacts_count = chat_page.get_contacts_count()
            
            if contacts_count > 0:
                chat_page.select_contact("Test")
                
                with allure.step("Отправить несколько сообщений"):
                    for i, message in enumerate(TestData.TEST_MESSAGES[:3]):
                        chat_page.send_message(message)
                        time.sleep(1)  # Ждем между сообщениями
                        
                with allure.step("Проверить отправку сообщений"):
                    # Проверяем, что последнее сообщение отправлено
                    last_message = chat_page.get_last_message()
                    assert TestData.TEST_MESSAGES[2] in last_message
                    chat_page.take_screenshot("send_multiple_messages")
            else:
                pytest.skip("Нет контактов для тестирования")
    
    @allure.title("Выход из системы")
    def test_logout(self):
        """Тест выхода из системы"""
        with allure.step("Выйти из системы"):
            chat_page = ChatPage(self.driver)
            chat_page.logout()
            
        with allure.step("Проверить выход"):
            login_page = LoginPage(self.driver)
            assert login_page.is_displayed(login_page.EMAIL_INPUT)
            chat_page.take_screenshot("logout")