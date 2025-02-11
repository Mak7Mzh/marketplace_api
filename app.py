from flask import Flask, request, send_file, jsonify
import json
import cfg, db_

app = Flask(__name__)

@app.route('/register/response', methods=['POST'])
def new_user():
    """ РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ """
    response_mess = {'response_server': []}
    print(f"Приход API: {request.get_json()}")  # Логирование тела запроса

    # Ожидаем данные в формате JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    phone_num = data.get('user_phoneNumber')
    user_real_name = data.get('user_real_name')
    pas = data.get('paswrd')

    response_bd = db_.chek_to_add_users(phone_num, pas, user_real_name)
    response_mess['response_server'].append({
        'message': response_bd
    })
    json.dumps(response_mess)
    if response_bd == 'good':
        return jsonify(response_mess), 200
    else:
        return jsonify(response_mess), 400


@app.route('/login/response', methods=['POST'])
def login_user():
    """ ЛОГИН ПОЛЬЗОВАТЕЛЯ """
    response_mess = {'response_server': []}
    print(f"Приход API: {request.get_json()}")  # Логирование тела запроса

    # Ожидаем данные в формате JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    log_in = data.get('login')
    pas = data.get('password')

    response_bd = db_.login_user(log_in, pas)
    print(response_bd)
    json.dumps(response_mess)
    if response_bd == 'error_password' or response_bd == 'error':
        response_mess['response_server'].append({
            'message': response_bd
        })
        print(response_mess, 2)
        return jsonify(response_mess), 400
    else:
        response_mess['response_server'].append({
            'user_phoneNumber': response_bd[0],
            'mail': response_bd[2],
            'user_real_name': response_bd[3]
        })
        print(response_mess, 1)
        return jsonify(response_mess), 200


@app.route('/users/get_all', methods=['GET'])
def get_all_user():
    return jsonify(db_.get_all_users())

@app.route('/get_all_product/response', methods=['GET'])
def get_all_products():
    """ ВЫВОД ВСЕХ ТОВАРОВ """
    response_bd = db_.get_all_product()
    if not isinstance(response_bd, list):
        response_mess = {'response_server': []}
        response_mess['response_server'].append({
            'message': response_bd
        })
        print(response_mess, 1)
        return json.dumps(response_mess)
    else:
        response_mess = {'response_server': response_bd}
        print(response_mess, 2)
        return json.dumps(response_mess)

""" MAIN """
if __name__ == '__main__':
    app.run(port=56500)