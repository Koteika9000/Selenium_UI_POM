from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from utilities.logging_config import logger
import allure

class Login_page(Base):
    
    urls = {
        "dev": "...",
        "prerelease": "...",
        "reserv": "...",
        "old_reserve": "...",
        "prod": "https://www.alexandar-cosmetics.com/"
    }

    credentials = {
        "default_buyer": {"email": "Kupibeton@rambler.ru", "password": "Beton2024"},
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

    personal_cabinet_button = "//div[@class='user-container']"
    login_choise_button = "//a[@class='btn btn-login ']"
    email_field = "//input[@name='_username']"
    password_field = "//input[@name='_password']"
    login_button = "//button[text()='Prijavite se']"
    user_name = "//span[contains(text(),'Petya')]"


    # Getters
    
    def get_personal_cabinet_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.personal_cabinet_button)))
    
    def get_login_choise_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_choise_button)))

    def get_email_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_login_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_button)))
    
    def get_user_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.user_name)))
    

    # Actions

    def click_personal_cabinet_button(self):
        self.get_personal_cabinet_button().click()
        logger.info("Клик на кнопку 'Личный кабинет'")

    def click_login_choise_button(self):
        self.get_login_choise_button().click()
        logger.info("Клик на кнопку 'Prijavite se'")

    def input_email_field(self, email):
        self.get_email_field().send_keys(email)
        logger.info("Введена электронная почта")
    
    def input_password_field(self, password):
        self.get_password_field().send_keys(password)
        logger.info("Введен Пароль")

    def click_login_button(self):
        self.get_login_button().click()
        logger.info("Клик на кнопку 'Войти'")

    
    # Methods

    def authorization(self):
        with allure.step(f"Авторизация в контуре {self.env} в роли {self.role}"):
            creds = self.credentials.get(self.role)
            if not creds:
                raise ValueError(f"Роль '{self.role}' не поддерживается.")
            self.driver.get(self.urls[self.env])
            # self.driver.maximize_window()
            self.click_personal_cabinet_button()
            self.click_login_choise_button()
            self.input_email_field(creds['email'])
            self.input_password_field(creds['password'])
            self.click_login_button()
            self.assert_contains_text(self.get_user_name(), 'Petya')
            logger.info("Авторизация прошла успешно")