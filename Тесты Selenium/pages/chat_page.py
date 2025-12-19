from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ChatPage(BasePage):
    # Локаторы
    CONTACTS_LIST = (By.CSS_SELECTOR, ".contact-item")
    SEARCH_CONTACTS_INPUT = (By.ID, "searchContacts")
    CURRENT_CHAT_USER = (By.ID, "currentChatUser")
    CHAT_MESSAGES = (By.ID, "chatMessages")
    MESSAGE_INPUT = (By.ID, "messageInput")
    SEND_BUTTON = (By.CSS_SELECTOR, "#messageForm button[type='submit']")
    LOGOUT_DROPDOWN = (By.CSS_SELECTOR, ".dropdown-toggle")
    LOGOUT_BUTTON = (By.LINK_TEXT, "Logout")
    ADMIN_LINK = (By.LINK_TEXT, "View Logs")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_contacts_count(self):
        """Получить количество контактов"""
        contacts = self.find_elements(self.CONTACTS_LIST)
        return len(contacts)
    
    def select_contact(self, contact_name):
        """Выбрать контакт по имени"""
        contacts = self.find_elements(self.CONTACTS_LIST)
        for contact in contacts:
            if contact_name.lower() in contact.text.lower():
                contact.click()
                return True
        return False
    
    def send_message(self, message):
        """Отправить сообщение"""
        if self.is_displayed(self.MESSAGE_INPUT):
            self.send_keys(self.MESSAGE_INPUT, message)
            self.click(self.SEND_BUTTON)
            time.sleep(1)  # Ждем отправки
            return True
        return False
    
    def get_last_message(self):
        """Получить последнее сообщение"""
        messages = self.find_elements((By.CSS_SELECTOR, "#chatMessages .message"))
        if messages:
            return messages[-1].text
        return ""
    
    def search_contact(self, search_text):
        """Поиск контакта"""
        self.send_keys(self.SEARCH_CONTACTS_INPUT, search_text)
        time.sleep(1)  # Ждем фильтрации
    
    def logout(self):
        """Выйти из системы"""
        self.click(self.LOGOUT_DROPDOWN)
        self.click(self.LOGOUT_BUTTON)
        
    def go_to_admin(self):
        """Перейти в админку"""
        self.click(self.LOGOUT_DROPDOWN)
        self.click(self.ADMIN_LINK)