import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

URL = 'https://passport.yandex.ru/auth/'
CORRECT_LOGIN ='homutovan2013@yandex.ru'
UNCORRECT_LOGIN = 'netology_test_2020@yandex.ru'
PWD = 'кецукнцкнцкцукнцукнцукнцнц'

class TestYandexPass(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get(URL)
        
    def test_correct_page(self):
        self.assertTrue('Авторизация' in self.driver.title)
        
    def test_correct_login(self):
        elem = self.driver.find_element_by_name('login')
        elem.send_keys(CORRECT_LOGIN)
        elem.send_keys(Keys.RETURN)
        self.assertTrue(self.driver.find_element_by_name('passwd'))
   
    def test_uncorrect_login(self):
        elem = self.driver.find_element_by_name('login')
        elem.send_keys(UNCORRECT_LOGIN)
        elem.send_keys(Keys.RETURN)
        self.assertTrue(self.driver.find_element_by_class_name('passp-form-field__error'))
        
    def test_correct_pwd(self):
        elem = self.driver.find_element_by_name('login')
        elem.send_keys(CORRECT_LOGIN)
        elem.send_keys(Keys.RETURN)
        self.assertTrue(self.driver.find_element_by_name('passwd'))
        elem = self.driver.find_element_by_name('passwd')
        elem.send_keys(PWD)
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        self.assertTrue('Управление аккаунтом' in self.driver.page_source)
        
    def test_uncorrect_pwd(self):
        elem = self.driver.find_element_by_name('login')
        elem.send_keys(CORRECT_LOGIN)
        elem.send_keys(Keys.RETURN)
        self.assertTrue(self.driver.find_element_by_name('passwd'))
        elem = self.driver.find_element_by_name('passwd')
        elem.send_keys(PWD + 'qwerty')
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        self.assertTrue('Неверный пароль' in self.driver.page_source)