import pypyodbc


def connect():# Функция для подключения к БД
    driver = 'DRIVER={SQL Server};'
    server = 'SERVER=DSHON\PROTEST;'
    db = 'DATABASE=trenerdb;'
    user = 'UID=dshon;'
    pw = 'PWD=dsgjvybnt*%'
    charset = 'utf8'
    conn_str = ';'.join([driver, server, db, user, pw, charset])
    global conn
    conn = pypyodbc.connect(conn_str)


####################################################
#Запросы БД
###################################################
def sql_zapros_id(id_us): # Запрос ID пользователя
    cursor = conn.cursor()
    cursor.execute(""" SELECT id 
                            FROM users 
                            WHERE id = %s """ % id_us)
    global user_id
    users = cursor.fetchone()
    if users is not None:
        user_id = users[0]
    else:
        user_id = users

    cursor.close()
    conn.close()


def zapros_name(id_us):# Запрос Имени пользователя
    cursor = conn.cursor()
    cursor.execute(""" SELECT name 
                       FROM users 
                       WHERE id = %s """ % id_us)

    global user_name
    users_n = cursor.fetchone()
    if users_n is not None:
        user_name = users_n[0]
    else:
        user_name = users_n
    cursor.close()
    conn.close()
    return


def zapros_punkt(id_us): # Запрос метки \Нужен для того что бы понять на какой ступене находится пользователь в бд
    cursor = conn.cursor()
    cursor.execute(""" SELECT metka 
                           FROM users 
                           WHERE id = %s """ % id_us)

    global metka
    metka = cursor.fetchone()
    cursor.close()
    conn.close()
    return


def zapros_dan(today, id_us): # Запрос данных в таблице замер\Нужен для того что бы понять как заполнять данные
    cursor = conn.cursor()
    cursor.execute(""" SELECT date, id 
                                                FROM zamer 
                                                WHERE date = ? and id = ? """, (today, id_us))

    dan = cursor.fetchone()
    if dan is None:
        cursor.execute("INSERT INTO  zamer  (date,id) VALUES (?,?)", (today, id_us))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()
    return


def zapros_dan_tren(today, id_us): # Запрос данных в таблице замер\Нужен для того что бы понять как заполнять данные
    cursor = conn.cursor()
    cursor.execute(""" SELECT date, id 
                                                FROM zamer 
                                                WHERE date = ? and id = ? """, (today, id_us))

    dan = cursor.fetchone()
    if dan is None:
        cursor.execute("INSERT INTO  zamer  (date,id) VALUES (?,?)", (today, id_us))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()
    return


def zapros_statistika(id_us): # Запрос статистики в бд
    cursor = conn.cursor()
    cursor.execute(""" SELECT date, Шея, Плечи, Руки, Грудь, Талия, Ягодицы, Бедра, Икры, Вес
                           FROM zamer 
                           WHERE id = %s  ORDER BY date""" % id_us)

    global statistica
    statistica = cursor.fetchall()
    cursor.close
    conn.close()
    return

###############################
#Функции добавление данных в БД
###############################


def add_id_name(name_us, id_us): # Добавление ID, метки  и имени пользователя в БД
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (id) VALUES ('%s')" % id_us)
    cursor.execute('UPDATE users SET name= ?, metka = ? WHERE  id = ? ', (name_us,0, id_us))
    conn.commit()
    cursor.close()
    conn.close()


def add_name(id_us, name): # Изменение имени и метки пользователя в БД
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name= ?, metka = ? WHERE  id = ? ', (name,0, id_us))
    conn.commit()
    cursor.close()
    conn.close()


def add_par(check, today, id_us, parametr):# Добавление Параметров пользователя в БД
    cursor = conn.cursor()
    try:
        if check == "Шея":
                cursor.execute('UPDATE zamer SET Шея= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
                conn.commit()
        elif check =='Плечи':
            cursor.execute('UPDATE zamer SET Плечи= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Руки':
            cursor.execute('UPDATE zamer SET Руки= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Грудь':
            cursor.execute('UPDATE zamer SET Грудь= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Талия':
            cursor.execute('UPDATE zamer SET Талия= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Ягодицы':
            cursor.execute('UPDATE zamer SET Ягодицы= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Бедра':
            cursor.execute('UPDATE zamer SET Бедра= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Икры':
            cursor.execute('UPDATE zamer SET Икры= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()
        elif check == 'Вес':
            cursor.execute('UPDATE zamer SET Вес= ? WHERE  id = ? and date = ?', (parametr, id_us, today))
            conn.commit()

        conn.commit()
        cursor.close()
        conn.close()

    except:
        cursor.close()
        conn.close()


def add_metk(punkt, id_us): # Добавление ID  и имени пользователя в БД
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET metka= ?  WHERE id= ? ', (punkt, id_us))
    conn.commit()
    cursor.close()
    conn.close()


