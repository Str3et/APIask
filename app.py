from flask import Flask
from flask import jsonify, render_template, make_response

from utils import test_email_reg, test_account_reg, add_account_result, add_email_result
from config import CACHE

app = Flask(__name__)


#  рендерит стартовую страницу
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html'), 200


# результат запроса пользователя по email
@app.route('/askAPI/find_email/<user_input_email>', methods=['GET'])
def email_exists_response(user_input_email: str):
    # проверка кэша, если такой адрес есть, выдавать из него, без запроса к ask.fm
    if CACHE.get(user_input_email) == 'exists':
        return jsonify({'server_response': 'exists'})

    else:
        response = test_email_reg(user_input_email)
        if response is True:
            add_email_result(user_input_email, 'exists')  # запись в БД
            CACHE.set(user_input_email, 'exists')  # запись в кэш успешного запроса
            return jsonify({'server_response': 'exists'})

        elif response is False:
            add_email_result(user_input_email, 'not_found')
            return jsonify({'server_response': 'not_found'})

        else:
            return jsonify(response)


# результат запроса пользователя по аккаунту
@app.route('/askAPI/find_account/<user_input_account>', methods=['GET'])
def account_exists_response(user_input_account: str):
    if CACHE.get(user_input_account) == 'exists':
        return jsonify({'server_response': 'exists'})

    else:
        response = test_account_reg(user_input_account)
        if response is True:
            add_account_result(user_input_account, 'exists')
            CACHE.set(user_input_account, 'exists')
            return jsonify({'server_response': 'exists'})

        else:
            add_account_result(user_input_account, 'not_found')
            return jsonify({'server_response': 'not_found'})


# 404 error
@app.errorhandler(404)
def not_found(error):
    response = {'server_response': 'error', 'reason': 'page_not_found'}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
