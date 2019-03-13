import re
import os
from selenium import webdriver

from config import BASE_URL
from mongo_db import email_db
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
        driver_browser.get(BASE_URL)
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
def add_result(email, status):
    email_db.insert_one({'user_registration_data': email, 'status': status})
