import re
import os
import requests
import string
import random
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from config import BASE_URL_ACCOUNT, TITLE_ACCOUNT, BASE_URL_FIND_LINK, BASE_URL_NEW_ACC
from mongo_db import data_db
import time

webdriver_settings = webdriver.ChromeOptions()
# webdriver_settings.add_argument('--headless')



def test_user_input(user_input: str):
    """ Проверяем регистрацию на сайте ask.fm с почты, введенной пользователем.

    :param user_input: str
        email адрес, который пользователь хочет проверить
    :return: dict
        результат проверки, обернутый в словарь, для передачи в JSON
    """

    # проверка соответствия email адреса стандарту
    mail = re.findall(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0]+$', user_input.lower())
    response = {}  # будущий ответ на запрос

    if mail:
        # вэбдрайвер Chrome для селениума
        driver_browser = webdriver.Chrome(os.getcwd() + '/chromedriver', chrome_options=webdriver_settings)
        rnd_email = ''.join(random.choices(string.ascii_letters, k=10))

        try:

            driver_browser.get(BASE_URL_NEW_ACC)  # переход на страницу входа
            time.sleep(2)

            new_acc_form_submit = driver_browser.find_element_by_id('signupNewForm')  # форма регистрации

            new_acc_form = driver_browser.find_element_by_id('user_email')
            new_acc_form.send_keys(f'{rnd_email}@aruy.ru')
            time.sleep(1)

            new_acc_form = driver_browser.find_element_by_id('user_name')
            new_acc_form.send_keys(f'{rnd_email}')
            time.sleep(1)

            new_acc_form = driver_browser.find_element_by_id('user_password')
            new_acc_form.send_keys('yura2525ARUY')
            time.sleep(1)

            new_acc_form = Select(driver_browser.find_element_by_id('user_gender_id'))
            new_acc_form.select_by_value('2')
            time.sleep(1)

            new_acc_form = Select(driver_browser.find_element_by_id('date_day'))
            new_acc_form.select_by_value('25')
            new_acc_form = Select(driver_browser.find_element_by_id('date_month'))
            new_acc_form.select_by_value('5')
            new_acc_form = Select(driver_browser.find_element_by_id('date_year'))
            new_acc_form.select_by_value('1990')
            time.sleep(2)

            new_acc_form_submit.submit()
            time.sleep(5)

            driver_browser.get(BASE_URL_FIND_LINK)  # переход на страницу поиска друзей
            form_find_link = driver_browser.find_element_by_name('q')
            form_find_link.send_keys(user_input)  # ввод email`a для поиска
            time.sleep(2)

            account_link = driver_browser.find_elements_by_css_selector('a.userItem_content')
            if account_link:
                for acc in account_link:
                    response['account_link'] = str(acc.get_attribute('href'))  # получение ссылки на аккаунт


            driver_browser.get(response['account_link'] + '/avatar')

            # avatar_name = driver_browser.find_element_by_xpath("//span[@class='userName']")

            # with open(os.path.join("image", f'avatar_{avatar_name.text}.png'), "wb") as file:
            #     file.write(driver_browser.find_element_by_class_name('userAvatar').screenshot_as_png)

            time.sleep(2)


        except:
            response['request canceled'] = 'sorry, the entrance is blocked'  # заблокировали вход на сайт

        finally:
            driver_browser.close()

        user_input_account = user_input.split('@')[0]  # отделяем додоменное имя для теста
        replace_symbol = re.compile("[^a-zA-Z,\d]")  # формула для замены символов в логине
        user_input_account = replace_symbol.sub("_", user_input_account)  # замена символов

        test = requests.get(BASE_URL_ACCOUNT + user_input_account)  # переход на страницу аккаунта
        dom = BeautifulSoup(test.text)  # получаем html страницы
        title = str(dom.select('title')[0])  # забираем строку tittle`a

        if title == TITLE_ACCOUNT:
            response['exists'] = False
        else:
            response['exists'] = True

        return response  # возвращаем результат проведенной проверки

    else:
        return {'server_response': 'error', 'reason': 'invalid_input'}  # возврат при ошибочном вводе адреса


def add_result(result: dict):
    """ Добавление данных в БД.

    :param result: dict
        словарь с результатами проверки пользовательского ввода
    """
    data_db.insert_one(dict(result))
    # print(res.inserted_id)
