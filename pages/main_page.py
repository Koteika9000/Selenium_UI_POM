from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from selenium.webdriver.common.action_chains import ActionChains
import time
from utilities.logging_config import logger
import allure

class Main_page(Base):
    
    urls = {
        "dev": "...",
        "prerelease": "...",
        "reserv": "...",
        "old_reserve": "...",
        "prod": "https://hudsonstore.com/"
    }

    credentials = {
        "default_byuer": {"login": "", "password": ""},
        "admin": {"login": "...", "password": "..."},
        "smm": {"login": "...", "password": "..."},
        "dev": {"login": "...", "password": "..."},
    }
        
    def __init__(self, driver, role, env, take_screenshot=None):
        super().__init__(driver)
        self.driver = driver
        self.role   = role.lower()
        self.env = env.lower()
        self.take_screenshot = take_screenshot
                
    # Locators

    main_header_img = "//img[@title='']"
    personal_cabinet_button = "//a[@title='Личный кабинет']"
    email_login_field = "//input[@id='emailLoginInput']"
    password_field = "//input[@id='passwordLoginInput']"
    login_button = "//button[@id='popup-login-button']"

    # Getters

    def get_main_header_img(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.main_header_img)))
    
    def get_personal_cabinet_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.personal_cabinet_button)))

    def get_email_login_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_login_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_login_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_button)))
    

    # Actions

    def click_personal_cabinet_button(self):
        self.get_personal_cabinet_button().click()
        logger.info("Клик на кнопку 'Личный кабинет'")

    def input_email_login_field(self, email):
        self.get_email_login_field().send_keys(email)
        logger.info("Введена электронная почта")
    
    def input_password_field(self, password):
        self.get_password_field().send_keys(password)
        logger.info("Введен Пароль")

    def click_login_button(self):
        button = self.get_login_button()
        logger.info("Клик на кнопку 'Войти'")

    
    # Methods

    def authorization(self):
        with allure.step(f"Авторизация в контуре {self.env} в роли {self.role}"):
            creds = self.credentials.get(self.role)
            if not creds:
                raise ValueError(f"Роль '{self.role}' не поддерживается.")
            self.driver.get(self.urls[self.env])
            self.driver.maximize_window()
            self.assert_contains_text(self.get_main_header_img(), '')
            self.click_personal_cabinet_button()
            self.input_email_login_field(creds['login'])
            self.input_password_field(creds['password'])
            self.click_login_button()
            # self.assert_contains_text(self.get_arm_header(), '')
            logger.info("Авторизация прошла успешно")