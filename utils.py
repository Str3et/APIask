import re
import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver

from config import BASE_URL_EMAIL, BASE_URL_ACCOUNT, TITLE_ACCOUNT
from mongo_db import data_db
import time

webdriver_settings = webdriver.ChromeOptions()
webdriver_settings.add_argument('--headless')
webdriver_settings.add_argument('--disable-gpu')
webdriver_settings.add_argument('--no-sandbox')
webdriver_settings.add_argument('--disable-dev-shm-usage')


# проверка введных пользователем данных на сайте.
def test_user_input(user_input):
    # проверка соответствия email адреса
    mail = re.findall(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0]+$', user_input.lower())
    response = {}  # будущий ответ на запрос

    if mail:
        # вэбдрайвер Chrome для селениума
        driver_browser = webdriver.Chrome(os.getcwd() + '/chromedriver', chrome_options=webdriver_settings)
        driver_browser.get(BASE_URL_EMAIL)
        form_email = driver_browser.find_element_by_class_name('inputForm')  # поиск по html
        form_email.send_keys(user_input)  # ввод email`a
        form_email.submit()  # отправка формы
        time.sleep(2)  # задержка браузера, для прогрузки формы

        try:
            # поиск события, которое выдает JS после проверки формы
            form_email = driver_browser.find_element_by_xpath("//*[@class='flash-message notice']")
            if form_email:
                response['email_response'] = 'exists'
        except:
            response['email_response'] = 'not_found'
        finally:
            driver_browser.close()

        user_input_account = user_input.split('@')[0]  # отделяем додоменное имя для теста
        test = requests.get(BASE_URL_ACCOUNT + user_input_account)  # переход на страницу аккаунта
        dom = BeautifulSoup(test.text)  # получаем html страницы
        title = str(dom.select('title')[0])  # забираем строку tittle`a

        if title == TITLE_ACCOUNT:
            response['account_response'] = 'not_found'
        else:
            response['account_response'] = 'exists'

        return response  # возвращаем результат проведенной проверки

    else:
        return {'server_response': 'error', 'reason': 'invalid_input'}  # возврат при ошибочном ввоже адреса


# Добавление нового документа в БД
def add_result(result):
    data_db.insert_one({'email_response': result['email_response'], 'account_response': result['account_response']})
