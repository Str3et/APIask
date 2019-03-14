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
    user_input_account = user_input_email.split('@')[0]

    # проверка кэша, если такой адрес есть, выдавать из него, без запроса к ask.fm
    if CACHE.get(user_input_email) == 'exists':
        return jsonify({'server_response': 'exists'})

    else:
        response_email = test_email_reg(user_input_email)
        if response_email == {'server_response': 'error', 'reason': 'invalid_input'}:
            return jsonify(response_email)
        response_account = test_account_reg(user_input_account)
        if response_email and response_account is True:
            return jsonify({'email_response': 'exists', 'account_response': 'exists'})
            # add_email_result(user_input_email, 'exists')  # запись в БД
            # CACHE.set(user_input_email, response)  # запись в кэш успешного запроса

        if response_email and response_account is False:
            return jsonify({'email_response': 'not_found', 'account_response': 'not_found'})

        if response_email is True and response_account is False:
            return jsonify({'email_response': 'exists', 'account_response': 'not_found'})

        if response_email is False and response_account is True:
            return jsonify({'email_response': 'not_found', 'account_response': 'exists'})

        # else:
        #     return jsonify(response_email)


# 404 error
@app.errorhandler(404)
def not_found(error):
    response = {'server_response': 'error', 'reason': 'page_not_found'}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    app.run()
