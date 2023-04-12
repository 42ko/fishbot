from datetime import date
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials



# Данные авторизации Google API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(creds)

# Открытие таблицы
sheet = client.open_by_key(googlesheet_id)

# Создание бота
bot = telebot.TeleBot(bot_token)

# markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# markup.add('Отмена')

# Определение функции для получения имени пользователя
@bot.message_handler(commands=['start'])
def get_name(message):
    # Отправка сообщения и запрос имени пользователя
    bot.send_message(message.chat.id, "Привет, я бот! Моя задача - заполнять таблицу вместо вас. Введите ваше имя, пожалуйста")
    bot.register_next_step_handler(message, get_procedure_name)

# Определение функции для получения названия процедуры
def get_procedure_name(message):
    name = message.text
    # Отправка сообщения и запрос названия процедуры
    bot.send_message(message.chat.id, "Введите название процедуры")
    bot.register_next_step_handler(message, lambda m: get_start_time(m, name))

# Определение функции для получения времени начала процедуры
def get_start_time(message, name):
    procedure_name = message.text
    # Отправка сообщения и запрос времени начала процедуры
    bot.send_message(message.chat.id, "Введите время начала процедуры в формате ЧЧ:ММ")
    bot.register_next_step_handler(message, lambda m: get_end_time(m, name, procedure_name))

# Определение функции для получения времени окончания процедуры и записи данных в таблицу
def get_end_time(message, name, procedure_name):
    start_time = message.text
    # Отправка сообщения и запрос времени окончания процедуры
    bot.send_message(message.chat.id, "Введите время окончания процедуры в формате ЧЧ:ММ")
    bot.register_next_step_handler(message, lambda m: save_data(m, name, procedure_name, start_time))

# Определение функции для сохранения данных в Google Таблицу
def save_data(message, name, procedure_name, start_time):
    end_time = message.text
    day = date.today().strftime("%d.%m.%Y")    
    row = [day, name, procedure_name, start_time, end_time]
    sheet.sheet1.append_row(row)
    bot.send_message(message.chat.id, "Данные успешно записаны в таблицу")
    bot.clear_step_handler(message)

# Запуск бота
bot.polling()