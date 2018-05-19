import telebot
import constants
import conectsql
import datetime
from datetime import date
import matplotlib.pyplot as plt
import os
"""
#proxy
proxy = urllib.request.ProxyHandler({'http': '191.241.251.194:20183'})
opener = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener)
urllib.request.urlopen('https://api.telegram.org/')
"""
bot = telebot.TeleBot(constants.token)
# Старт бота и запрос id  на существование


def us_name(message):  # функция изменения имени
    id_us = message.chat.id
    name = message.text  # получаем введенное имя
    conectsql.connect()  # подключение к БД
    conectsql.add_name(id_us, name)  # Вызов функции перезаписи имени в бд
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # создаем клавиатуру
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, 'Имя изменено, для перехода в меню нажмите кнопку"',
                                           reply_markup=user_markup)
    # отправление сообщения и кнопки
    return


def add_zamer(message):  # Запись введенных параметров замеров

    id_us = message.chat.id
    try:
        parametr = int(message.text)  # Получение введенных параметров
        conectsql.connect()  # Подключение к БД
        conectsql.zapros_punkt(id_us)  # Вызов фунции запроса  метки
        check = conectsql.metka[0]  # достать метку из картеджа
        today = date.today()  # получение даты отправленого замера
        if check == 'Шея'or 'Плечи' or 'Руки' or 'Грудь' or 'Талия' or 'Ягодицы' or 'Бедра' or 'Икры' or 'Вес':
            conectsql.connect()  # подключение к бд
            conectsql.zapros_dan(today, id_us)  # вызов функции запроса данных из таблицы zamer
            conectsql.connect()  # подключение к бд
            conectsql.add_par(check, today, id_us, parametr)  # Вызов функции добавление параметров замеров
        else:
            bot.send_message(message.chat.id, 'Приветствую тебя ,')
    except:
        bot.send_message(message.chat.id, 'Вы ввели неверные данные. Попробуйте еще раз')
        handle_reg(message)
    return


@bot.message_handler(commands=['start'])  # Бот реагирует на каманду /start
def handle_reg(message):
    id_us = message.from_user.id  # Получение индификатора пользователя
    name_us = message.from_user.first_name  # Получение имени пользователя зарегестрированного в телеграмме
    conectsql.connect()  # Подключение к БД
    conectsql.sql_zapros_id(id_us)  # Запрос на наличие id в БД
    z_id = conectsql.user_id    # Получение Id из бд или None

    if message.text == "/start":
        if z_id is None:     # Проверка ID
            conectsql.connect()    # Подключение к БД
            conectsql.add_id_name(name_us, id_us)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # создаем клавиатуру
            user_markup.row('Журнал тренировок', 'Статистика и замеры')
            user_markup.row('Программы', 'База упражнений')
            user_markup.row('Настройка')
            bot.send_message(message.chat.id, 'Приветствую тебя ,' + name_us + '!\nОбрати внимание на панель кнопок.'
                                              'Выберите интересующую вас функцию, или выберите команду /help '
                                              'и я объясню  как это работает', reply_markup=user_markup)
            # отправление сообщения и кнопки
        else:
            conectsql.connect()   # Подключение к БД
            conectsql.zapros_name(id_us)   # Запрос имени из БД
            nameus = conectsql.user_name   # Получение имени из БД

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
            user_markup.row('Журнал тренировок', 'Статистика и замеры')
            user_markup.row('Программы', 'База упражнений')
            user_markup.row('Настройка')
            bot.send_message(message.chat.id, 'Приветствую тебя ,' + nameus + '!\nОбрати внимание на панель кнопок.'
                                              'Выберите интересующую вас функцию, или выберите команду /help '
                                              'и я объясню  как это работает', reply_markup=user_markup)
            # Отправка сообщения и клавиатуры


@bot.message_handler(content_types=['text'])  # Бот реагирует на отправленное сообщение в типе TEXT
def handle_workspace(message):   # Фунция рабочей области
    id_us = message.chat.id

    if message.text == 'Меню':
        conectsql.connect()  # Подключение к БД
        conectsql.zapros_name(id_us)  # Запрос имени из БД
        nameus = conectsql.user_name  # Получение имени из БД

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Журнал тренировок', 'Статистика и замеры')
        user_markup.row('Программы', 'База упражнений')
        user_markup.row('Настройка')
        bot.send_message(message.chat.id, 'Приветствую тебя ,' + nameus + '!\nОбрати внимание на панель кнопок.'
                                          'Выберите интересующую вас функцию, или выберите команду /help '
                                          'и я объясню  как это работает', reply_markup=user_markup)

    elif message.text == "Журнал тренировок":     # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Добавить упражнение')
        user_markup.row('Просмотор моей тренировки')
        user_markup.row('Меню')
        bot.send_message(message.chat.id,   'Выберите вид тренеровкок'
                                            ' для того что бы  я смог рассчитать необходимую нагрузки,',
                                            reply_markup=user_markup)  # отправка сообщения и клавиатуры

    elif message.text == "Добавить упражнение":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Силовая тренировка')
        user_markup.row('Набор мышечной массы')
        user_markup.row('Нужно похудеть')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, "Выберите необходимый для вас вид тренировки",
                                          reply_markup=user_markup)

    elif message.text == 'Просмотор моей тренировки':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Показать тренировку')
        user_markup.row('Расчитать следующую тренировку')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, "В данном разделе вы можете просмотреть свою последнюю тренировку,"
                                          "и так же я могу рассчитать показатели следующей тренировки,"
                                          "для того что бы сохранить его в свой дневник", reply_markup=user_markup)

    elif message.text == 'Силовая тренировка':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('1 подход', '2 подход')
        user_markup.row('3 подход', '4 подход')
        user_markup.row('5 подход', '6 подход')
        user_markup.row('7 подход', '8 подход')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите подход и введите данные', reply_markup=user_markup)

    elif message.text == 'Набор мышечной массы':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('1 подход', '2 подход')
        user_markup.row('3 подход', '4 подход')
        user_markup.row('5 подход', '6 подход')
        user_markup.row('7 подход', '8 подход')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите подход и введите данные', reply_markup=user_markup)

    elif message.text == 'Тренировка для похудения':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('1 подход', '2 подход')
        user_markup.row('3 подход', '4 подход')
        user_markup.row('5 подход', '6 подход')
        user_markup.row('7 подход', '8 подход')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите подход и введите данные', reply_markup=user_markup)

    elif message.text == '1 подход' or message.text == '2 подход' or message.text == '3 подход' or \
        message.text == '4 подход' or message.text == '5 подход' or message.text == '6 подход' or \
        message.text == '7 подход' or message.text == '8 подход':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Вес')
        user_markup.row('Колличество повтореий')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите соответствующую кнопку и введите параметр,что бы я смог записать',
                                          reply_markup=user_markup)

    elif message.text == 'Статистика и замеры':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите раздел и впишите свои параметры', reply_markup=user_markup)
        # отправка сообщения и клавиатуры

    elif message.text == 'Шея':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Плечи':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Руки':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Грудь':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Талия':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Ягодицы':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Бедра':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Икры':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Шея', 'Плечи', 'Руки')
        user_markup.row('Грудь', 'Талия', 'Ягодицы')
        user_markup.row('Бедра ', 'Икры', 'Вес')
        user_markup.row('Результат с последних замеров')
        user_markup.row('Меню')
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры', reply_markup=user_markup)
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Вес':  # действие при нажатие кнопки
        punkt = message.text  # Получене имени кнопки для создание метки
        conectsql.connect()  # Подключение к БД
        conectsql.add_metk(punkt, id_us)  # Вызов функции занесения етки в БД
        msg = bot.send_message(message.chat.id, 'Введите параметры')
        bot.register_next_step_handler(msg, add_zamer)  # Отправка сообщения и переход к ф-ции

    elif message.text == 'Результат с последних замеров':  # действие при нажатие кнопки
        data_names = ["Шея(см)", "Плечи(см)", "Руки(см)", "Грудь(см)", "Талия(см)", "Ягодицы(см)", "Бедра(см)",
                      "Икры(см)", "Вес(кг)"]
        name_graf = str(message.chat.id)
        directory = 'C:/graf'
        conectsql.connect()  # Подключение к БД
        conectsql.zapros_statistika(id_us)
        par = conectsql.statistica
        x = [row[0] for row in par]
        y1 = [row[1] for row in par]
        y2 = [row[2] for row in par]
        y3 = [row[3] for row in par]
        y4 = [row[4] for row in par]
        y5 = [row[5] for row in par]
        y6 = [row[6] for row in par]
        y7 = [row[7] for row in par]
        y8 = [row[8] for row in par]
        y9 = [row[9] for row in par]
        # будет 1 график, на нем 4 линии:

        fig, ax = plt.subplots(figsize=(12.3, 8))
        # функция y1(x), синий, надпись y(x)
        ax.scatter(x, y1, color="Yellow")
        ax.plot(x, y1, color="Yellow")
        # функция y2(x), красный, надпись y'(x)
        ax.scatter(x, y2, color="Green")
        ax.plot(x, y2, color="Green")
        # функция y3(x), зеленый, надпись y''(x)
        ax.scatter(x, y3, color="Blue")
        ax.plot(x, y3, color="Blue")
        # функция y3(x), зеленый, надпись y''(x)
        ax.scatter(x, y4, color="Brown")
        ax.plot(x, y4, color="Brown")
        ax.scatter(x, y5, color="Red")
        ax.plot(x, y5, color="Red")
        ax.scatter(x, y6, color="Orange")
        ax.plot(x, y6, color="Orange")
        # функция y2(x), красный, надпись y'(x)
        ax.scatter(x, y7, color="Pink")
        ax.plot(x, y7, color="Pink")
        # функция y3(x), зеленый, надпись y''(x)
        ax.scatter(x, y8, color="Gray")
        ax.plot(x, y8, color="Gray")
        # функция y3(x), зеленый, надпись y''(x)
        ax.scatter(x, y9, color="purple")
        ax.plot(x, y9, color="purple")
        # подпись у горизонтальной оси х
        ax.set_xlabel("Дата замеров")
        # подпись у вертикальной оси y
        ax.set_ylabel("Параметры замеров")
        # показывать условные обозначения
        ax.grid()
        ax.legend(data_names, bbox_to_anchor=(1, 0), loc="lower right", bbox_transform=fig.transFigure, ncol=9)
        fig.savefig('C:/graf/' + name_graf)

        all_file = os.listdir(directory)
        for file in all_file:
            if file == name_graf + '.png':
                img = open(directory + '/' + file, 'rb')  # Открываем карточку в двоичном виде
                bot.send_chat_action(message.from_user.id, 'upload_photo')
                bot.send_photo(message.from_user.id, img)
                img.close()

    elif message.text == "Программы":  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Пример Силовых тренировок')
        user_markup.row('Пример Тренировок на массу')
        user_markup.row('Пример Тренировка для похудения')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, 'Выберите раздел и я поясню в чем смысл данной тренировки,'
                                          'так же я покажу вам примеры тренировок', reply_markup=user_markup)

    elif message.text == "База упражнений":  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Упражнения на шею')
        user_markup.row('Упражнения на плечи')
        user_markup.row('Упражнения на руки')
        user_markup.row('Упражнения на грудь')
        user_markup.row('Упражнения на талию')
        user_markup.row('Упражнения на ягодицы')
        user_markup.row('Упражнения на бедра')
        user_markup.row('Упражнения на икры')
        user_markup.row('Меню')
        bot.send_message(message.chat.id, "Выберите группу мышц и я покажу вам базовые "
                                          "упражнения", reply_markup=user_markup)
        # отправка сообщения и клавиатуры

    elif message.text == 'Настройка':  # действие при нажатие кнопки
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)  # Создание клавиатуры
        user_markup.row('Изменить Имя')
        user_markup.row('Меню')
        bot.send_message(message.from_user.id, 'Для изменения имени нажмите  "Изменить Имя"',
                         reply_markup=user_markup)  # отправка сообщения и клавиатуры

    elif message.text == 'Изменить Имя':
        pro = bot.send_message(message.chat.id, "Введите имя")
        bot.register_next_step_handler(pro, us_name)


def main():
    while 1 == 1:  # Условие 1=1 используется, чтобы программа выполнялась всегда
        try:
            bot.polling(none_stop=True, interval=2, timeout=300)
        except ConnectionResetError or ConnectionError:     # Если есть ошибка соединения, то будет выведена
                                                            # дата и время ошибки, но бот будет стараться подключиться
                print(datetime.date.today())


if __name__ == '__main__':
    main()