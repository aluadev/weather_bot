import telebot
from telebot.types import ReplyKeyboardMarkup
import requests
from datetime import date

#token = '968254774:AAGtxRgK9AWZldMPFXOfGbEmRfGhPYyiJiI'
token = '1317198475:AAHqm43exCftREeFWt5HVyXLirwGECZ3PRc'
bot = telebot.TeleBot(token)
api_url = 'https://stepik.akentev.com/api/weather'
states = {}
city = None
buttons = ['today', 'tomorrow', 'day after tomorrow', '2 days after tomorrow', 'check for another city']
MAIN_STATE = 'main'
NEXT_STATE = 'next_state'
DATE_STATE = 'weather_date'


def get_temp(city_name, n_day):
    city_param = requests.get(
        api_url,
        params={'city': str(city_name), 'forecast': n_day}
    ).json()
    city_temp = str(round(city_param['temp']))+' grad'
    return city_temp


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = message.from_user.id
    state = states.get(user_id, MAIN_STATE)
    if state == MAIN_STATE:
        start_handler(message)
    elif state == NEXT_STATE:
        weather_handler(message)
    elif state == DATE_STATE:
        weather_date_handler(message)


def start_handler(message):
    if message.text == '/start':
        bot.reply_to(message, "This is weather-bot. I will help you to know about the weather in any city. Which city you are interested in?")
        states[message.from_user.id] = NEXT_STATE


def weather_handler(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(*buttons)
    bot.send_message(message.from_user.id, 'Choose the day?', reply_markup=markup)
    states[message.from_user.id] = DATE_STATE


def weather_date_handler(message):
    req_date = message.text
    current_day = date.today().day
    if req_date == 'today':
        req_day = current_day
    elif req_date == 'tomorrow':
        req_day = current_day + 1
    elif req_date == 'day after tomorrow':
        req_day = current_day + 2
    elif req_date == '2 days after tomorrow':
        req_day = current_day + 3
    elif req_date == 'check for another city':
        states[message.from_user.id] = MAIN_STATE
    if req_date != 'check for another city':
        for i in range(4):
            if (req_day - current_day) == i:
                n_day = i
        city_temp = get_temp(city, n_day)
        bot.reply_to(message, city_temp)
bot.polling()
