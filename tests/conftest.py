import pytest
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utilities.logging_config import logger
import time
import allure
import platform

# Инициализация, настройка и закрытие драйвера браузера
@pytest.fixture
def setup_driver():
    logger.info(" Запуск драйвера")

    project_root = Path(__file__).resolve().parent.parent
    os_name = platform.system()

    if os_name == "Linux":
        driver_path = project_root / 'utilities' / 'chromedriver'
    elif os_name == "Windows":
        driver_path = project_root / 'utilities' / 'chromedriver.exe'
    else:
        raise ValueError(f"Операционная система {os_name} не поддерживается")
    
    logger.info(f"Выбран драйвер для {os_name}: {driver_path}")

    download_dir = str(project_root / 'downloads')

    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': download_dir}
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('detach', True) 

    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://reports.ksomb.fortus.pro")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.close()
    logger.info(" Драйвер закрыт")

# Фикстура для создания скриншотов по запросу
@pytest.fixture
def take_screenshot(setup_driver, request):
    def _take_screenshot(screenshot_name="manual_screenshot"):
        project_root = Path(__file__).resolve().parent.parent
        screenshot_dir = project_root / 'screenshots'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        # Формируем имя файла с именем теста и пользовательским именем
        timestamp = int(time.time())
        test_name = request.node.name
        screenshot_path = str(screenshot_dir / f"{screenshot_name}_{test_name}_{timestamp}.png")
        
        try:
            setup_driver.save_screenshot(screenshot_path)
            logger.info(f"Скриншот сохранен: {screenshot_path}")
            with open(screenshot_path, 'rb') as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Скриншот ({screenshot_name})",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            logger.error(f"Не удалось сохранить скриншот {screenshot_path}: {e}")
        
        return screenshot_path
    
    return _take_screenshot


# Настройка выбора ролей и контура
def pytest_addoption(parser):
    parser.addoption(
        "--role", action="store", default="operator",
        help="Роль для тестов: operator, mailer, iogv1, iogv2, iogv3"
    )
    parser.addoption(
        "--env", action="store", default="dev",
        help="Выбор окружения: dev, prerelease, reserv, prod"
    )

@pytest.fixture
def role(request):
    return request.config.getoption("--role")

@pytest.fixture
def env(request):
    return request.config.getoption("--env")

# Старт и окончание логирования. Скриншоты в случае ошибок (с отправкой в Allure)

def pytest_runtest_setup(item):
    logger.info(f"Setup for test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    logger.info(f"Teardown for test: {item.name}")

def pytest_exception_interact(node, call, report):
    if report.failed:
        exc_info = call.excinfo
        logger.error(f"Test {node.name} failed with {exc_info.typename}: {exc_info.value}")
        driver = node.funcargs.get("setup_driver")
        if driver:
# Захват ошибок консоли браузера при провале теста
            try:
                console_logs = driver.get_log("browser")
                for log in console_logs:
                    if log.get("level") in ["ERROR", "SEVERE"]:
                        logger.error(f"Ошибка в консоли браузера в тесте {node.name}: {log['message']}")
            except Exception as e:
                logger.error(f"Не удалось захватить логи консоли браузера: {e}")

# Скриншоты в случае ошибок (с отправкой в Allure)
            project_root = Path(__file__).resolve().parent.parent
            screenshot_dir = project_root / 'screenshots'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            screenshot_path = str(screenshot_dir / f"error_screenshot_{node.name}_{int(time.time())}.png")
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
                with open(screenshot_path, 'rb') as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"Скриншот ошибки ({node.name})",
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as e:
                logger.error(f"Failed to save screenshot {screenshot_path}: {e}")