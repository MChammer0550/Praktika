import random
import string

class TestData:
    @staticmethod
    def generate_email(prefix="test"):
        """Сгенерировать уникальный email"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{prefix}_{random_str}@example.com"
    
    @staticmethod
    def generate_name(prefix="Test"):
        """Сгенерировать имя"""
        random_str = ''.join(random.choices(string.ascii_lowercase, k=6))
        return f"{prefix}{random_str.capitalize()}"
    
    # Тестовые данные
    VALID_USER = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "Test123!"
    }
    
    INVALID_USER = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    
    ADMIN_USER = {
        "email": "admin@example.com",
        "password": "Admin123!"
    }
    
    TEST_MESSAGES = [
        "Hello, this is a test message!",
        "How are you today?",
        "Testing messenger functionality",
        "This is another test message",
        "Final test message"
    ]