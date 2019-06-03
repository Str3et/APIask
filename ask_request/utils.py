import re
import os
import requests
import string
import random
from bs4 import BeautifulSoup
from pprint import pprint

from config import BASE_URL, TITLE_ACCOUNT
from mongo_db import data_db


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

        rnd_email = ''.join(random.choices(string.ascii_letters, k=10))

        try:

            # testing = {}

            session = requests.Session()  # создание сессии
            r = session.get(f'{BASE_URL}signup')
            dom = BeautifulSoup(r.text)  # распарсили страницу регистрации

            find_token = dom.find('input', attrs={'name': 'authenticity_token'})  # находим токен для регистрации
            token = find_token['value']
            # testing['token'] = token

            params = {
                'user[email]': f'{rnd_email}@aruy.ru',
                'user[name]': rnd_email,
                'user[login]': f'{rnd_email}25456',
                'user[password]': 'yura2525ARUY',
                'user[gender_id]': '2',
                'user[born_at_day]': '25',
                'user[born_at_month]': '5',
                'user[born_at_year]': '2000',
                'user[language_code]': 'en',
                'authenticity_token': token,
            }

            session.post(f'{BASE_URL}signup', data=params)

            # testing['email'] = rnd_email
            # testing['first_stat'] = reg_r.status_code

            friends_r = session.get(f'{BASE_URL}account/friends', params={'q': user_input}) # ищем пользователя

            after_login = BeautifulSoup(friends_r.text)
            account_link = after_login.find('a', attrs={'class': 'userItem_content'})
            if account_link: # если пользователь существует пишем ссылку и находим аватарку
                response['account_link'] = BASE_URL + account_link['href']

                avatar_name = str(account_link['href']).replace('/', '')
                avatar = session.get(BASE_URL + account_link['href'] + '/avatar')
                after_avatar = BeautifulSoup(avatar.text)

                find_avatar = after_avatar.find('img')
                if find_avatar['src'][-4:] == '.jpg': # забираем только .jpg
                    with open(os.path.join("image", f'avatar_{avatar_name}.jpg'), "wb") as target:
                        a = requests.get(find_avatar['src'])
                        target.write(a.content)
                        response['avatar'] = f'http://127.0.0.1:5000/askAPI/download/avatar_{avatar_name}.jpg'

            # pprint(testing)

        except:
            response['request canceled'] = 'sorry, the entrance is blocked'  # заблокировали вход на сайт


        user_input_account = user_input.split('@')[0]  # отделяем додоменное имя для теста
        replace_symbol = re.compile("[^a-zA-Z,\d]")  # формула для замены символов в логине
        user_input_account = replace_symbol.sub("_", user_input_account)  # замена символов

        r = requests.get(BASE_URL + user_input_account)  # переход на страницу аккаунта
        dom = BeautifulSoup(r.text)  # получаем html страницы
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
