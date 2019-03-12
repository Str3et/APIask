from flask import Flask
from flask import jsonify, render_template, make_response

from utils import test_email_reg, add_result
from config import CACHE


app = Flask(__name__)


#  рендерит стартовую страницу
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html'), 200


# результат запроса пользователя
@app.route('/askAPI/find_email/<user_input_email>', methods=['GET'])
def email_exists_response(user_input_email: str):
    print(CACHE.get(user_input_email))
    response = test_email_reg(user_input_email)

    if response is True:
        add_result(user_input_email, 'exists')
        CACHE.set(user_input_email, 'exists')
        return jsonify({'server_response': 'exists'})

    elif response is False:
        add_result(user_input_email, 'not_found')
        return jsonify({'server_response': 'not_found'})

    else:
        return jsonify(response)


# 404 error handler
@app.errorhandler(404)
def not_found(error):
    response = {'server_response': 'error', 'reason': 'page_not_found'}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    app.run()


# задание следующее:
# написать апи на фласк, которое проверяет наличие аккаунта по почте на сайте ask.fm
# и так же ищет аккаунт по додоменной части почтового адреса (то что до собаки)
# сделать кэширование успешных запросов на час
# готовую работу выложит на гитхаб
# и развернуть на любом хостинге для тестов
