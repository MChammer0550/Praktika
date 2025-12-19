from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class AdminPage(BasePage):
    # Локаторы
    START_DATE_INPUT = (By.ID, "Filter_StartDate")
    END_DATE_INPUT = (By.ID, "Filter_EndDate")
    IP_ADDRESS_INPUT = (By.ID, "Filter_IpAddress")
    GROUP_BY_IP_CHECKBOX = (By.ID, "Filter_GroupByIp")
    GROUP_BY_DATE_CHECKBOX = (By.ID, "Filter_GroupByDate")
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    MESSAGES_TABLE = (By.CSS_SELECTOR, "table tbody tr")
    EXPORT_JSON_BUTTON = (By.LINK_TEXT, "Export as JSON")
    LOGS_TABLE = (By.TAG_NAME, "table")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/Admin/Logs"
        
    def open(self):
        """Открыть админ страницу"""
        self.driver.get(f"{self.driver.current_url.split('/')[0]}//{self.driver.current_url.split('/')[2]}{self.url}")
        
    def apply_filters(self, start_date=None, end_date=None, ip_address=None, group_by_ip=False, group_by_date=False):
        """Применить фильтры"""
        if start_date:
            self.send_keys(self.START_DATE_INPUT, start_date)
        
        if end_date:
            self.send_keys(self.END_DATE_INPUT, end_date)
            
        if ip_address:
            self.send_keys(self.IP_ADDRESS_INPUT, ip_address)
            
        if group_by_ip:
            checkbox = self.find_element(self.GROUP_BY_IP_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
                
        if group_by_date:
            checkbox = self.find_element(self.GROUP_BY_DATE_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
                
        self.click(self.APPLY_FILTERS_BUTTON)
        time.sleep(2)  # Ждем применения фильтров
        
    def get_messages_count(self):
        """Получить количество сообщений в таблице"""
        rows = self.find_elements(self.MESSAGES_TABLE)
        return len(rows)
    
    def export_to_json(self):
        """Экспортировать данные в JSON"""
        self.click(self.EXPORT_JSON_BUTTON)