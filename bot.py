import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('5191273277:AAHyxVdMro_qXDyCAsm5PhL6riQVx7O_eHQ')

w = requests.get('https://rp5.ru/Погода_в_Яровом,_Алтайский_край')
nphw = requests.get('https://prognoz3.ru/россия/алтайский-край/погода-в-яровом/почасовая')

bs1 = BeautifulSoup(w.content, "html.parser")
bs2 = BeautifulSoup(nphw.content, "html.parser")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!" + "\n" "Список всех команд: " + "\n" "/weather" + " - погода в текущее время")


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Поиск данных...')
    weather_value = bs2.find('div', class_='ArchiveTemp').find('span', class_='t_0').text + " (Ощущается как " + bs2.find('div', class_='TempStr').find('span', class_='t_0').text + ") " + bs2.find("div", class_="b-weather_current_additional").find("span", class_="note").text.lower() + "\n"
    pressure_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="pressure").text + " мм.рт.ст" + "\n"
    humidity_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="humidity").text + "\n"
    wind_speed_value = bs2.find('div', class_='b-weather_current_additional').find("span", class_="wind").text
    bot.send_message(message.chat.id, "Погода: " + weather_value + pressure_value + humidity_value + wind_speed_value)


@bot.message_handler(commands=['password_generator'])
def password_generator(message):
    bot.send_message(message.chat.id, 'Введите количество символов для пароля')


bot.polling()
