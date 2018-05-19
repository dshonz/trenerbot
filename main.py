bot = telebot.TeleBot(const.token) #Подключение к API Telegram

def sqloutputting(sqltext, sqlarg): #Функция выполнения SQL-запроса на выдачу информации
myconnect = pypyodbc.connect('Driver={SQL Server};' #Подключение в БД 
'Server=' + const.sqlserv + ';'
'Database=' + const.sqlDB + ';')
cursor = myconnect.cursor() #Создание курсора, который будет работать с базой данных
quare = (sqltext) #Текст SQL-запроса
arg = sqlarg #Аргументы SQL-запроса
cursor.execute(quare, arg) #Выполнение SQL-запроса
answer = cursor.fetchall() #Вывод результата SQL-запроса в переменную
myconnect.close() #Закрытие соединения с базой данных
return answer #Возвращение результатов SQL-запроса в основную программу

def sqlinputting(sqltext, sqlarg):
myconnect = pypyodbc.connect('Driver={SQL Server};' #Подключение в БД 
'Server=' + const.sqlserv + ';'
'Database=' + const.sqlDB + ';')
cursor = myconnect.cursor() #Создание курсора, который будет работать с базой данных
quare = (sqltext) #Текст SQL-запроса
arg = sqlarg #Аргументы SQL-запроса
cursor.execute(quare, arg) #Выполнение SQL-запроса
myconnect.commit() #Сохраниение изменений в базе данных
myconnect.close()

def checkuser(idTelegram, nameUser): #Функция проверки нового пользователя
arg = ()
test = sqloutputting(const.searchUser, arg) #Вызов функции поиска пользователей
for row in test:
if idTelegram == row[0]:
return #Если в базе есть такой пользователь, то возвращаемся к основной программе
arg = (idTelegram, nameUser, '3', '0', '0', '0', '0') #Аргументы для внесения в таблицу пользователей: ID пользователя и его имя
sqlinputting(const.newUser, arg) #Вызов функции занесения данных в бД
return

def action(idTelegram, action): #Функция сохранения действия пользователя для статистики
arg = (datetime.datetime.now(), idTelegram, action)
sqlinputting(const.newAction, arg)
return

def newKartocka(idTelegram, kartDir, kolvokart, date, text):
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message(idTelegram, const.obr,
reply_markup=keyboard) #Отправка сообщения и клавиатуры
directory = kartDir #Директория где хранятся вопросы по теме "Искусство"
all_file = os.listdir(directory) #Смотрим все файлы в директории
randomch = random.randint(1, (int(kolvokart))) #Случайное число от 1 до 97 - номер карточки
for file in all_file:
if file == str(randomch) + '.png': #Находм нужную карточку
img = open(directory + '/' + file, 'rb') #Открываем карточку в двоичном виде
bot.send_chat_action(idTelegram,
'upload_photo') #Отправляем действие, что бот отправляет изображение
bot.send_photo(idTelegram, img) #Отправляем саму карточку
img.close()
arg = (text, date, str(randomch), idTelegram)
sqlinputting(const.newKart, arg)

def otvKartoch(idTelegram, kartDir, nomkart):
directory = kartDir #Директория где хранятся вопросы по теме "Искусство"
all_file = os.listdir(directory) #Смотрим все файлы в директории
for file in all_file:
if file == str(nomkart) + '-1.png': #Находм нужную карточку
img = open(directory + '/' + file, 'rb') #Открываем карточку в двоичном виде
bot.send_chat_action(idTelegram,
'upload_photo') #Отправляем действие, что бот отправляет изображение
bot.send_photo(idTelegram, img) #Отправляем саму карточку
img.close()

@bot.message_handler(commands=["start"]) #Команда /start
def handle_start(message):
checkuser(message.from_user.id, message.from_user.first_name) # Вызов функции проверки пользователя
keyboard = types.ReplyKeyboardMarkup(True, True) # Создание программируемой клавиатуры
keyboard.row('Что было в этот день раньше', 'Хочу играть')
keyboard.row('О проекте', 'Обратная связь')
bot.send_message(message.from_user.id, const.Hi, reply_markup=keyboard) # Отправка сообщения и клавиатуры
arg = ('0', message.from_user.id)
sqlinputting(const.action,
arg)

@bot.message_handler(content_types=["text"])
def handle_start(message):
action(message.from_user.id, message.text) #Сохраниение действия пользователя для создания статистиики
arg = (message.from_user.id,)
metka = sqloutputting(const.metka, arg)[0][0] #Просмотр метки действия пользователя
if metka == 'feedback':
if message.text == 'Главное меню': #Срабатывает при нажатие кнопки "Главное меню" или команды /start
checkuser(message.from_user.id, message.from_user.first_name) #Вызов функции проверки пользователя
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Что было в этот день раньше', 'Хочу играть')
keyboard.row('О проекте', 'Обратная связь')
bot.send_message(message.from_user.id, const.Hi, reply_markup=keyboard) #Отправка сообщения и клавиатуры
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
else:
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message('492277596', 'Был оставлен отзыв: ' + message.text, reply_markup=keyboard)
bot.send_message(message.from_user.id, 'Спасибо за оставленнный отзыв', reply_markup=keyboard)
elif metka =='nick':
name = message.text
arg = (name, message.from_user.id)
sqlinputting(const.newNick, arg)
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
bot.send_message(message.from_user.id, 'Никнейм успешно изменен')
bot.send_message(message.from_user.id, const.GameStart,
reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif metka == 'art': #Проверяем ответ если был
try:
arg = (message.from_user.id,)
dannie = sqloutputting(const.dannie, arg)
arg =(dannie[0][0],)
otvet = sqloutputting(const.otvetart, arg)[0][0]
razndate = message.date - dannie[0][1]
razn = abs(int(message.text)-otvet)
score = 1.1
if razn > 1000: #Расчет баллов от точности ответа
score = 0
elif razn > 500:
score = 1
elif razn > 250:
score = 2
elif razn > 125:
score = 4
elif razn > 80:
score = 5
elif razn > 40:
score = 7
elif razn > 20:
score = 9
elif razn > 10:
score = 10
elif razn > 5:
score = 12
elif razn < 5:
score = 13
if razndate > 120: #Расчет баллов от скорости ответа
score = score*0.9
elif razndate > 60:
score = score*1
elif razndate > 30:
score = score*1.2
elif razndate > 20:
score = score*1.3
elif razndate < 20:
score = score*1.5
otvKartoch(message.from_user.id, 'D:/TimeLine/Искуство/otvet', dannie[0][0])
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Играть еще', 'Главное меню')
bot.send_message(message.from_user.id, 'Вы заработали '+str(int(score)) +' очк.', reply_markup=keyboard) #Отправка сообщения и клавиатуры
score = score+dannie[0][2]
arg = (score, message.from_user.id)
sqlinputting(const.newScore, arg) #Обновление счета игрока в БД
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
except:
bot.send_message(message.from_user.id, 'Введите корректные данные')
elif metka == 'liter': #Проверяем ответ если был
try:
arg = (message.from_user.id,)
dannie = sqloutputting(const.dannie, arg)
arg =(dannie[0][0],)
otvet = sqloutputting(const.otvetliter, arg)[0][0]
razndate = message.date - dannie[0][1]
razn = abs(int(message.text)-otvet)
score = 1.1
if razn > 1000: #Расчет баллов от точности ответа
score = 0
elif razn > 500:
score = 1
elif razn > 250:
score = 2
elif razn > 125:
score = 4
elif razn > 80:
score = 5
elif razn > 40:
score = 7
elif razn > 20:
score = 9
elif razn > 10:
score = 10
elif razn > 5:
score = 12
elif razn < 5:
score = 13
if razndate > 120: #Расчет баллов от скорости ответа
score = score*0.9
elif razndate > 60:
score = score*1
elif razndate > 30:
score = score*1.2
elif razndate > 20:
score = score*1.3
elif razndate < 20:
score = score*1.5
otvKartoch(message.from_user.id, 'D:/TimeLine/Литература/Otvet', dannie[0][0])
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Играть еще', 'Главное меню')
bot.send_message(message.from_user.id, 'Вы заработали '+str(int(score)) +' очк.', reply_markup=keyboard) #Отправка сообщения и клавиатуры
score = score+dannie[0][2]
arg = (score, message.from_user.id)
sqlinputting(const.newScore, arg) #Обновление счета игрока в БД
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
except:
bot.send_message(message.from_user.id, 'Введите корректные данные')
elif message.text == 'О проекте' or message.text == '/about': #Срабатывает при нажатие кнопки "О проекте" или команды /about
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Мы в ВК', 'Instagram')
keyboard.row('Обратная связь', 'Главное меню')
bot.send_message(message.from_user.id, const.about, reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Главное меню' or message.text == '/start': #Срабатывает при нажатие кнопки "Главное меню" или команды /start
checkuser(message.from_user.id, message.from_user.first_name) #Вызов функции проверки пользователя
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Что было в этот день раньше', 'Хочу играть')
keyboard.row('О проекте', 'Обратная связь')
bot.send_message(message.from_user.id, const.Hi, reply_markup=keyboard) #Отправка сообщения и клавиатуры
arg = ('0', message.from_user.id)
sqlinputting(const.action, arg) #Обнуление метки действия пользователя
elif message.text == 'Обратная связь' or message.text == '/feedback':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, const.feedback, reply_markup=keyboard) #Отправка сообщения и клавиатуры
arg = ('feedback', message.from_user.id)
sqlinputting(const.action, arg) #Создание метки действия пользователя
elif message.text == 'Мы в ВК':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Мы в ВК', 'Instagram')
keyboard.row('Обратная связь', 'Главное меню')
bot.send_message(message.from_user.id, 'https://vk.com/linetimeprojecct';, reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Instagram':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Мы в ВК', 'Instagram')
keyboard.row('Обратная связь', 'Главное меню')
bot.send_message(message.from_user.id, 'https://www.instagram.com/linetimeproject/';, reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Хочу играть' or message.text == '/game' or message.text == 'Играть еще':
arg = (message.from_user.id,)
nick = sqloutputting(const.nick, arg)[0][0]
name = sqloutputting(const.nick, arg)[0][1]
if nick == '0':
keyboard = types.ReplyKeyboardMarkup(True, True)
keyboard.row('Оставить', 'Ввести иной')
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Ваш никней оставить ' + name +
' или хотите ввести другой', reply_markup=keyboard)
else:
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, const.GameStart,
reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Оставить':
name = sqloutputting(const.nick, arg)[0][1]
arg = (name, message.from_user.id)
sqlinputting(const.newNick, arg)
keyboard =
types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, const.GameStart,
reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Ввести иной' or message.text == 'Изменить никнейм':
arg = ('nick', message.from_user.id)
sqlinputting(const.action, arg) #Создание метки действия пользователя
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Напишите какой никнейм вы хотите использовать',
reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Правила игры':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Хочу играть')
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, const.regulation, reply_markup=keyboard) #Отправка сообщения и клавиатуры
elif message.text == 'Рейтинг': #Вывод топ рейтинга
arg=()
reit = sqloutputting(const.reit, arg) #Получение списка имен и счета пользователей
i = 0
k = 0
reiting = ''
while k < 5: #В цикле ниже получение списка топ5 игроков
reiting = reiting + str(k+1)+'. ' + reit[k][0]+' - '+str(reit[k][1])+' очк. \n'
if reit[k][2] == message.from_user.id:
i=1 #Проверка, если в топе данный игрок
k=k+1
if i==0: #Если он не в топ5 то игрок записывается отдельной стокой
arg = (message.from_user.id,)
reit = sqloutputting(const.reitmy, arg)
reiting = reiting + ' \n' + reit[0][0] + ' - ' + str(reit[0][1]) + ' очк.'
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, reiting, reply_markup=keyboard)
elif message.text == 'Искусство':
newKartocka(message.from_user.id, 'D:/TimeLine/Искуство/vopros', '97', message.date, 'art')
elif message.text == 'Музыка':
#newKartocka(message.from_user.id, 'D:/TimeLine/Искуство/vopros', '97', message.date)
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
elif message.text == 'Кино':
#newKartocka(message.from_user.id, 'D:/TimeLine/Искуство/vopros', '97', message.date)
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
elif message.text == 'Литература':
newKartocka(message.from_user.id, 'D:/TimeLine/Литература/vopros', '106', message.date, 'liter')
elif message.text == 'Все темы':
#newKartocka(message.from_user.id, 'D:/TimeLine/Искуство/vopros', '97', message.date)
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Рейтинг', 'Все темы')
keyboard.row('Искусство', 'Музыка')
keyboard.row('Кино', 'Литература')
keyboard.row('Правила игры', 'Настройка', 'Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
elif message.text == 'Что было в этот день раньше':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
elif message.text == 'Настройка':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание
программируемой клавиатуры
keyboard.row('Изменить никнейм')
keyboard.row('Изменить отображение вопросов/ответов')
keyboard.row('Смена языка')
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Выберите пункт настроек', reply_markup=keyboard)
elif message.text == 'Смена языка':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Изменить никнейм')
keyboard.row('Изменить отображение вопросов/ответов')
keyboard.row('Смена языка')
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
elif message.text == 'Изменить отображение вопросов/ответов':
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Изменить никнейм')
keyboard.row('Изменить отображение вопросов/ответов')
keyboard.row('Смена языка')
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, 'Раздел находится в разработке', reply_markup=keyboard)
else:
keyboard = types.ReplyKeyboardMarkup(True, True) #Создание программируемой клавиатуры
keyboard.row('Главное меню')
bot.send_message(message.from_user.id, const.non, reply_markup=keyboard)

def main():
while 1==1: #Условие 1=1 используется, чтобы программа выполнялась всегда
try:
bot.polling(none_stop=True, interval=2, timeout=700)
except ConnectionResetError or ConnectionError: #Если есть ошибка соединения, то будет выведена дата и время ошибки, но бот будет стараться подключиться
print(datetime.date.today())

if __name__ == '__main__':
main()
