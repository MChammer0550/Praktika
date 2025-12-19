#!/usr/bin/env python3
"""
Скрипт для запуска тестов Selenium
"""

import subprocess
import sys
import os
from datetime import datetime

def run_tests(test_type="all", browser="chrome", headless=False):
    """
    Запуск тестов
    
    :param test_type: Тип тестов (all, login, registration, messaging, admin)
    :param browser: Браузер для тестов (chrome, firefox)
    :param headless: Запуск в headless режиме
    """
    
    # Создаем папки для отчетов
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"reports/{timestamp}"
    screenshot_dir = "screenshots"
    
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Параметры pytest
    pytest_args = [
        "pytest",
        "-v",
        f"--html={report_dir}/report.html",
        "--self-contained-html",
        f"--alluredir={report_dir}/allure-results"
    ]
    
    # Выбор тестов
    if test_type == "login":
        pytest_args.append("tests/test_login.py")
    elif test_type == "registration":
        pytest_args.append("tests/test_registration.py")
    elif test_type == "messaging":
        pytest_args.append("tests/test_messaging.py")
    elif test_type == "admin":
        pytest_args.append("tests/test_admin.py")
    else:
        pytest_args.append("tests/")
    
    # Переменные окружения для конфигурации
    env = os.environ.copy()
    env["BROWSER"] = browser
    env["HEADLESS"] = str(headless).lower()
    
    print(f"Запуск тестов: {test_type}")
    print(f"Браузер: {browser}")
    print(f"Headless: {headless}")
    print(f"Отчеты: {report_dir}")
    print("-" * 50)
    
    # Запуск тестов
    result = subprocess.run(pytest_args, env=env)
    
    # Генерация отчета Allure
    try:
        subprocess.run(["allure", "generate", f"{report_dir}/allure-results", "-o", f"{report_dir}/allure-report", "--clean"])
        print(f"Allure отчет сгенерирован: {report_dir}/allure-report/index.html")
    except:
        print("Allure не установлен. Установите: pip install allure-pytest")
    
    return result.returncode

if __name__ == "__main__":
    # Парсинг аргументов командной строки
    import argparse
    
    parser = argparse.ArgumentParser(description="Запуск Selenium тестов для мессенджера")
    parser.add_argument("--type", choices=["all", "login", "registration", "messaging", "admin"],
                       default="all", help="Тип тестов для запуска")
    parser.add_argument("--browser", choices=["chrome", "firefox"], 
                       default="chrome", help="Браузер для тестов")
    parser.add_argument("--headless", action="store_true", 
                       help="Запуск в headless режиме")
    
    args = parser.parse_args()
    
    # Запуск тестов
    exit_code = run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=args.headless
    )
    
    sys.exit(exit_code)