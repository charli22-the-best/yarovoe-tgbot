import telebot
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver

bot = telebot.TeleBot('5191273277:AAHyxVdMro_qXDyCAsm5PhL6riQVx7O_eHQ')
w = requests.get('https://rp5.ru/Погода_в_Яровом,_Алтайский_край')
bs1 = BeautifulSoup(w.content, "html.parser")

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!" + "\n" "Список всех команд: " + "\n" "/weather" + " - погода в текущее время")


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Поиск данных...')
    weather_info = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    geomagnetic = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    geomagnetic.get('https://www.gismeteo.ru/weather-yarovoye-11314/gm/')
    weather_info.get('https://yandex.ru/pogoda/yarovoe')
    weather_value = bs1.find('div', class_='ArchiveTemp').find('span', class_='t_0').text
    feeling = bs1.find('div', class_='TempStr').find('span', class_='t_0').text
    wind_speed = weather_info.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div[6]/div[1]/div[2]").text
    pressure = weather_info.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div[6]/div[3]/div[2]").text
    humidity = weather_info.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div[6]/div[2]").text
    geomagnetic_activity = geomagnetic.find_element_by_xpath(
        "/html/body/section[2]/div[1]/section[2]/div/div[1]/div[2]").text
    bot.send_message(message.chat.id,
                     "Погода: " + weather_value + " (Ощущается как " + feeling + ")" + "\n" "Ветер: " + wind_speed + "\n" "Влажность: " + humidity + "\n" 'Давление: ' + pressure + "\n" "Геомагнитная активность: " + geomagnetic_activity.lower())


@bot.message_handler(commands=['password_generator'])
def password_generator(message):
    bot.send_message(message.chat.id, 'Введите количество символов для пароля')


bot.polling()
