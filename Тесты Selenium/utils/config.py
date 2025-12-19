import os
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Config:
    BASE_URL = "https://localhost:7227"  # ИЗМЕНИТЕ ЭТУ СТРОКУ
    BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    SCREENSHOT_PATH = "screenshots"
    TEST_USER_EMAIL = "testuser@example.com"
    TEST_USER_PASSWORD = "Test123!"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "Admin123!"
    
    # Дополнительные настройки для локального HTTPS
    ACCEPT_INSECURE_CERTS = True
    IGNORE_SSL_ERRORS = True
    
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")