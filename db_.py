import psycopg2, random, json, cfg
from psycopg2 import errors


""" ПОДКЛЮЧЕНИЕ К БД """
def conncet_to_bd():
    try:
        conn = psycopg2.connect(database=cfg.name_db,
                                host="localhost",
                                user="postgres",
                                password=cfg.password_bd,
                                port="5432")

        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(e)
        return None, None

"""
======================================> МАНИПУЛЯЦИИ С ЮЗЕРОМ <=========================================
"""

def chek_to_add_users(ph_user, pas, user_realName, mail_, adress):
    """ ДОБАВЛЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ """
    try:
        conn, cur = conncet_to_bd()
        if conn is None or cur is None:
            print('chek_to_add_users -> неудальст подключится')
            return 'error'

        cur.execute("""SELECT user_phoneNumber FROM users WHERE user_phoneNumber = %s;""", (ph_user,))
        existing_user = cur.fetchone()
        if existing_user:
            conn.close()
            return 'error_user_phone_exist'

        response = new_user(ph_user, pas, user_realName, mail_, adress, conn, cur)

        return response

    except Exception as e:
        print(f'АШИБКА БЛИН chek_to_add_users -> :', e)
        return 'error'

def new_user(ph_user, pas, user_realName, mail_, adress, conn, cur):
    try:
        cur.execute("""INSERT INTO users (user_phoneNumber, user_real_name, paswrd, mail, user_adress) VALUES (%s, %s, %s, %s, %s);""", (ph_user, user_realName, pas, mail_, adress,))
        conn.commit()
        conn.close()
        return 'good'
    except errors.UniqueViolation as e:
        # Обработка ошибки уникальности
        conn.rollback()  # Откат транзакции
        print(f'Ошибка уникальности -> :', e)
        return 'error_user_mail_exists'
    except Exception as e:
        conn.rollback()
        print(f'АШИБКА БЛИН new_user -> :', e)
        return 'error'


def get_all_users():
    """ ПОЛУЧЕНИЕ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ """
    try:
        conn, cur = conncet_to_bd()
        result = {"users": []}
        if conn is None or cur is None:
            return json.dumps({"error": "error"})

        cur.execute("""SELECT * FROM users;""")
        users_list = cur.fetchall()
        conn.close()
        #print(users_list)

        for user in users_list:
            result['users'].append({
                'user_id': user[0],
                'user_phoneNumber': user[1],
                'user_real_name': user[2],
                'user_adress': user[3],
                'password': user[4],
                'mail': user[5]
            })

        return json.dumps(result)

    except Exception as e:
        print(f'АШИБКА БЛИН get_all_users ->:', e)
        return json.dumps({"error": str(e)})


def login_user(identifier, password):
    """ ЛОГИН ПОЛЬЗОВАТЕЛЯ """
    try:
        conn, cur = conncet_to_bd()
        if conn is None or cur is None:
            print('login_user -> не удалось подключиться')
            return 'error'

        cur.execute("""
            SELECT user_phoneNumber, paswrd, mail, user_real_name 
            FROM users 
            WHERE user_phoneNumber = %s OR mail = %s;
        """, (identifier, identifier))

        user_data = cur.fetchone()
        conn.close()

        if user_data:
            stored_password = user_data[1]
            print(user_data)
            print(f"Ответ бд: {user_data[1]} | Приход по Api: {password}")
            if str(stored_password) == str(password):
                return user_data
            else:
                print('login_user -> пароль неверный')
                return 'error_password'
        else:
            print('login_user -> пользователь не найден')
            return 'error'
    except Exception as e:
        print(f'ОШИБКА! login_user ->:', e)
        return 'error'


"""
====================================>  МАНИПУЛЯЦИИ С ТОВАРАМИ <=========================================
"""

def get_once_product_id(id_prod):
    """ ПОЛУЧЕНИЕ ОПРЕДЕЛЁННОГО ТОВАРА ПО ID"""
    try:
        conn, cur = conncet_to_bd()
        if conn is None or cur is None:
            print('get_once_product_id -> не удалось подключиться')
            return 'error'

        cur.execute("""
                    SELECT * 
                    FROM product 
                    WHERE pid = %s;
                """, (str(id_prod)))
        product_data = cur.fetchone()
        conn.close()

        if product_data:
            return product_data
        else:
            print('get_once_product_id -> трек не найден')
            return 'error_user'
    except Exception as e:
        print(f'ОШИБКА get_once_product_id ->:', e)
        return 'error'


def get_random_product():
    """ ПОЛУЧЕНИЕ 5 РАНДОМНЫХ ТОВАРА"""
    try:
        conn, cur = conncet_to_bd()
        if conn is None or cur is None:
            print('get_random_product -> не удалось подключиться')
            return 'error'


        cur.execute("""SELECT * FROM product""")
        productS_data = cur.fetchall()
        conn.close()
        ids = [list(item) for item in productS_data]

        # Выбираем случайные 5 ID
        random_ids = random.sample(ids, 5)

        return random_ids

    except Exception as e:
        print(f'ОШИБКА! get_random_product ->:', e)
        return 'error'

def get_all_product():
    """ ПОЛУЧЕНИЕ всех товаров по списку """
    try:
        conn, cur = conncet_to_bd()
        if conn is None or cur is None:
            print('get_random_product -> не удалось подключиться')
            return 'error'


        cur.execute("""SELECT * FROM product""")
        productS_data = cur.fetchall()
        conn.close()
        ids = [list(item) for item in productS_data]

        # Выбираем случайные 5 ID
        #random_ids = random.sample(ids, 5)

        return ids

    except Exception as e:
        print(f'ОШИБКА! get_random_product ->:', e)
        return 'error'

if __name__ == '__main__':
    conn, cur = conncet_to_bd()
    response_bd = new_user('45345435', '234123123', 'Андрюша', 'zhuhlin05@gmail.com','неважно', conn, cur)
    print(response_bd)