import time
from pages.login_page import Login_page
import pytest
from utilities.logging_config import logger
import allure

# @allure.id("")
# @allure.feature("")
# @allure.story("")
# @allure.title("")
# @allure.description("")
def test_schemes_tab(setup_driver, role, env, take_screenshot):

    if not role:
        pytest.fail("Роль не указана. Используйте --role=...")
    if not env:
        pytest.fail("Окружение не указано. Используйте --env=...")
    
    driver = setup_driver
    
    logger.info(f'... Контур: {env}, роль: {role}.')
    
    login = Login_page(driver, role, env, take_screenshot)
    login.authorization()
    # start = Main_page(driver, role, env, take_screenshot)
    # start.schemes_tab_test()
    # start.logout()

    logger.info("Тест ... успешно пройден!")