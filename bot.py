from email import message
import telebot
import requests
import random
from time import sleep
from bs4 import BeautifulSoup
from googletrans import Translator


bot = telebot.TeleBot('5191273277:AAHyxVdMro_qXDyCAsm5PhL6riQVx7O_eHQ')

w = requests.get('https://rp5.ru/Погода_в_Яровом,_Алтайский_край')
nphw = requests.get('https://prognoz3.ru/россия/алтайский-край/погода-в-яровом/почасовая')

bs1 = BeautifulSoup(w.content, "html.parser")
bs2 = BeautifulSoup(nphw.content, "html.parser")


# Начало

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!" + "\n" "Список всех команд: " + "\n" "/weather" + " - погода в текущее время" + "\n" "/password_generator" + " - генератор надёжных паролей")


# Погода

@bot.message_handler(commands=['weather'])
def weather(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, 'Поиск данных...')
        sleep(1)
        weather_value = bs1.find('div', class_='ArchiveTemp').find('span', class_='t_0').text + " (Ощущается как " + bs1.find('div', class_='TempStr').find('span', class_='t_0').text + "), " + bs2.find("div", class_="b-weather_current_additional").find("span", class_="note").text.lower() + "\n"
        pressure_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="pressure").text + " мм.рт.ст" + "\n"
        humidity_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="humidity").text + "\n"
        wind_speed_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="wind").text + "\n"
        long_sun = bs2.find("span", class_="b-weather_days_long").find("span", class_="sunrise").text + "\n" + bs2.find("span", class_="sunset").text
        bot.send_message(message.chat.id, "Погода: " + weather_value + pressure_value + humidity_value + wind_speed_value + long_sun)
    elif message.chat.type == "group" or message.chat.type == "supergroup":
        bot.reply_to(message, 'Поиск данных...')
        sleep(1)
        weather_value = bs1.find('div', class_='ArchiveTemp').find('span', class_='t_0').text + " (Ощущается как " + bs1.find('div', class_='TempStr').find('span', class_='t_0').text + "), " + bs2.find("div", class_="b-weather_current_additional").find("span", class_="note").text.lower() + "\n"
        pressure_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="pressure").text + " мм.рт.ст" + "\n"
        humidity_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="humidity").text + "\n"
        wind_speed_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="wind").text + "\n"
        long_sun = bs2.find("span", class_="b-weather_days_long").find("span", class_="sunrise").text + "\n" + bs2.find("span", class_="sunset").text
        bot.reply_to(message, "Погода: " + weather_value + pressure_value + humidity_value + wind_speed_value + long_sun)


# Генератор_паролей

@bot.message_handler(commands=['password_generator'])
def password_generator(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        bot.reply_to(message, 'Нельзя пользоваться данной командой в группах!' + "\n" "Пишите в личные сообщения @Yarovoe_bot" + "\n" + "\n" "Мы заботимся о вашей безопасности")
    if message.chat.type == "private":
      msg = bot.send_message(message.from_user.id, 'Введите количество символов для пароля')
      bot.register_next_step_handler(msg, answer_password_generator)

def answer_password_generator(message):
    pas = ''
    for x in range(int(f"{message.text}")): #Количество символов (16)
        pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ')) #Символы, из которых будет составлен пароль
    bot.send_message(message.chat.id, "Ваш пароль:")
    bot.send_message(message.chat.id, pas)

# Переводчик

translator = Translator()

@bot.message_handler(commands="translate")
def send_text(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='RU',callback_data=1))
    markup.add(telebot.types.InlineKeyboardButton(text='EN ', callback_data=2))
    markup.add(telebot.types.InlineKeyboardButton(text='DE ', callback_data=3))

    bot.send_message(message.chat.id, "Выбери язык на который хотите перевести текст.", reply_markup = markup)

def next_trans2(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'ru'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

def next_trans3(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'en'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans4(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'DE'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == '1':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=5))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans2)
    elif call.data == '2':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=5))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans3)
    elif call.data == '3':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=5))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans4)
    elif call.data == '4':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='RU',callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='EN ', callback_data=2))
        markup.add(telebot.types.InlineKeyboardButton(text='DE ', callback_data=3))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Выбери язык на который хотите перевести текст.", reply_markup = markup)
    elif call.data == '5':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Перевод', callback_data=4))
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Вы вернулись в главное меню!", reply_markup = markup)
      



bot.polling()