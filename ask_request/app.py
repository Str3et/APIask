from flask import Flask
from flask import jsonify, render_template, make_response
from flask import send_from_directory

from utils import test_user_input, add_result
from config import CACHE

app = Flask(__name__)


#  рендерит стартовую страницу
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html'), 200


# результат запроса пользователя по email
@app.route('/askAPI/find_info/<user_input>', methods=['GET'])
def email_acc_exists_response(user_input: str):
    # проверка кэша, если такой адрес есть, выдавать из него, без запроса к ask.fm
    if CACHE.get(user_input) is not None:
        return jsonify(CACHE.get(user_input))

    response = test_user_input(user_input)
    if response.get('reason'):
        return jsonify(response)
    else:
        CACHE.set(user_input, response)  # запись в кэш успешного запроса
        add_result(response)  # запись в БД
        return jsonify(response)


@app.route('/askAPI/download/<filename>')
def download(filename):
    return send_from_directory('image/', filename)


# 404 error
@app.errorhandler(404)
def not_found(error):
    response = {'server_response': 'error', 'reason': 'page_not_found'}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    app.run()
