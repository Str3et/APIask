import re
import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver

from config import BASE_URL_EMAIL, BASE_URL_ACCOUNT, TITLE_ACCOUNT
from mongo_db import email_db, account_db
import time

webdriver_settings = webdriver.ChromeOptions()
webdriver_settings.add_argument('--headless')
webdriver_settings.add_argument('--disable-gpu')
webdriver_settings.add_argument('--no-sandbox')
webdriver_settings.add_argument('--disable-dev-shm-usage')


# проверка введного пользователем email`a на регистрацию на сайте.
def test_email_reg(email):
    mail = re.findall(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0]+$', email.lower())  # проверка соответствия адреса

    if mail:
        # вэбдрайвер Chrome для селениума
        driver_browser = webdriver.Chrome(os.getcwd() + '/chromedriver', chrome_options=webdriver_settings)
        driver_browser.get(BASE_URL_EMAIL)
        form_email = driver_browser.find_element_by_class_name('inputForm')  # поиск по html
        form_email.send_keys(email)  # ввод email`a
        form_email.submit()  # отправка формы
        time.sleep(2)  # задержка для браузера, для прогрузки формы

        try:
            # поиск события, которое выдает JS после проверки формы
            form_email = driver_browser.find_element_by_xpath("//*[@class='flash-message notice']")
            if form_email:
                return True
        except:
            return False
        finally:
            driver_browser.close()

    else:
        return {'server_response': 'error', 'reason': 'invalid_input'}  # возврат при ошибочном ввоже адреса


# Добавление нового документа в БД
def add_email_result(email, status):
    email_db.insert_one({'user_registration_data': email, 'status': status})


def add_account_result(account, status):
    email_db.insert_one({'user_registration_data': account, 'status': status})


def test_account_reg(account_name):
    # post_result = requests.post(BASE_URL_ACCOUNT, data=account_name)
    test = requests.get(BASE_URL_ACCOUNT + account_name)
    dom = BeautifulSoup(test.text)  # получаем html страницы
    title = str(dom.select('title')[0])  # забираем строку tittle`a
    if title == TITLE_ACCOUNT:
        return False
    else:
        return True

