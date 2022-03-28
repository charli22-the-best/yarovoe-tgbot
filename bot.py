import telebot
from telebot import types
import requests
from time import sleep
from bs4 import BeautifulSoup
import random
from gc import callbacks
from googletrans import Translator
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


bot = telebot.TeleBot('5191273277:AAHyxVdMro_qXDyCAsm5PhL6riQVx7O_eHQ')


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
weather1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
weather1.get('https://rp5.ru/Погода_в_Яровом,_Алтайский_край')
weather2 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
weather2.get('https://prognoz3.ru/россия/алтайсикй-край/погода-в-яровом/почасовая')


# Начало

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!" + "\n" "Список всех команд: " + "\n" "/weather" + " - погода в текущее время" + "\n" + "\n" "/password_generator" + " - генератор надёжных паролей" + "\n" + "\n" "/translate" + " - переводчик")

   

# Погода

@bot.message_handler(commands=['weather'])
def weather(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, 'Поиск данных...')
        sleep(1)
        weather_value = 'Погода: ' + weather1.find_element(By.XPATH, "//*[@id='archiveString']/div[1]").text + " (" + weather1.find_element(By.XPATH, "//*[@id='archiveString']/div[2]").text + ")" + "\n"
        pressure_value = 'Давление: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[6]").text + "\n"
        humidity_value = 'Влажность: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[7]").text + "\n"
        wind_speed_value = 'Ветер: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[8]").text + "\n"
        long_sun = weather2.find_element(By.XPATH, "//body/div[@class='b-wrapper']/div[@class='b-content']/div[@class='b-weather']/div[@class='b-weather_hourly']/div[1]/table[1]/caption[1]/span[2]/span[1]").text
        bot.send_message(message.chat.id, weather_value + pressure_value + humidity_value + wind_speed_value + long_sun)
    elif message.chat.type == "group" or message.chat.type == "supergroup":
        bot.reply_to(message, 'Поиск данных...')
        sleep(1)
        weather_value = 'Погода: ' + weather1.find_element(By.XPATH, "//*[@id='archiveString']/div[1]").text + " (" + weather1.find_element(By.XPATH, "//*[@id='archiveString']/div[2]").text + ")" + "\n"
        pressure_value = 'Давление: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[6]").text + "\n"
        humidity_value = 'Влажность: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[7]").text + "\n"
        wind_speed_value = 'Ветер: ' + weather2.find_element(By.XPATH, "//div[@class='b-weather_current scroll-yes']//div[1]//div[2]//span[8]").text + "\n"
        long_sun = weather2.find_element(By.XPATH, "//body/div[@class='b-wrapper']/div[@class='b-content']/div[@class='b-weather']/div[@class='b-weather_hourly']/div[1]/table[1]/caption[1]/span[2]/span[1]").text
        bot.reply_to(message, weather_value + pressure_value + humidity_value + wind_speed_value + long_sun)


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
        pas = pas + random.choice(list('+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')) #Символы, из которых будет составлен пароль
    bot.send_message(message.chat.id, "Ваш пароль:")
    bot.send_message(message.chat.id, pas)
    bot.send_message(message.chat.id,  'НИКОМУ НЕ СООБЩАЙТЕ ЕГО!')



# Переводчик

translator = Translator()

@bot.message_handler(commands="translate")
def send_text(message):
    if message.chat.type == "private":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton(text='RU (Русский)',callback_data='RU'),
            telebot.types.InlineKeyboardButton(text='EN (English)', callback_data='EN'),
            telebot.types.InlineKeyboardButton(text='DE (Deutsch)', callback_data='DE')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='UK (Український)', callback_data='UK'),
            telebot.types.InlineKeyboardButton(text='KK (қазақ)', callback_data='KK')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='ES (Español)', callback_data='ES'),
            telebot.types.InlineKeyboardButton(text='FR (Français)', callback_data='FR'),
            telebot.types.InlineKeyboardButton(text='IT (Italiano)', callback_data='IT')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='NL (Nederlands)', callback_data='NL'),
            telebot.types.InlineKeyboardButton(text='PL (Polski)', callback_data='PL'),
            telebot.types.InlineKeyboardButton(text='PT (Português)', callback_data='PT')
        )

        bot.send_message(message.chat.id, "Выбери язык на который хотите перевести текст", reply_markup = markup)

    else: 
        bot.reply_to(message, "На данный момент перевод в группах недоступен")

def next_trans_ru(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'RU'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

def next_trans_en(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'EN'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_de(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'DE'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_uk(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'UK'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_kk(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'KK'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_es(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'ES'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_fr(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'FR'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_it(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'IT'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_nl(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'NL'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_pl(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'PL'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)
def next_trans_pt(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'PT'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == 'RU':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_ru)
    elif call.data == 'EN':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_en)
    elif call.data == 'DE':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_de)
    elif call.data == 'UK':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_uk)
    elif call.data == 'KK':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_kk)
    elif call.data == 'ES':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_es)
    elif call.data == 'FR':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_fr)
    elif call.data == 'IT':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_it)
    elif call.data == 'NL':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_nl)
    elif call.data == 'PL':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_pl)
    elif call.data == 'PT':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data='menu'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data='translate'))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans_pt)
    elif call.data == 'menu':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton(text='RU (Русский)',callback_data='RU'),
            telebot.types.InlineKeyboardButton(text='EN (English)', callback_data='EN'),
            telebot.types.InlineKeyboardButton(text='DE (Deutsch)', callback_data='DE')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='UK (Український)', callback_data='UK'),
            telebot.types.InlineKeyboardButton(text='KK (қазақ)', callback_data='KK')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='ES (Español)', callback_data='ES'),
            telebot.types.InlineKeyboardButton(text='FR (Français)', callback_data='FR'),
            telebot.types.InlineKeyboardButton(text='IT (Italiano)', callback_data='IT')
        )
        markup.row(
            telebot.types.InlineKeyboardButton(text='NL (Nederlands)', callback_data='NL'),
            telebot.types.InlineKeyboardButton(text='PL (Polski)', callback_data='PL'),
            telebot.types.InlineKeyboardButton(text='PT (Português)', callback_data='PT')
        )
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Выбери язык на который хотите перевести текст", reply_markup = markup)
    elif call.data == 'translate':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Перевод', callback_data='menu'))
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Вы вернулись в главное меню!", reply_markup = markup)





bot.polling()