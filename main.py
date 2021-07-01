import requests
import re
import telebot
from telebot import types

bot = telebot.TeleBot('1786389601:AAFGiQAbYTcI4EAIZWchFgIjoZxIRqnTYKw')


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@bot.message_handler(commands=['dogs'])
def bop(message):
    url = get_image_url()
    bot.send_photo(message.chat.id, photo=url)


def reply():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('/dogs')
    markup.add(button_1)
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Для получения фото нажмите /dogs", reply_markup=reply())


@bot.message_handler(content_types=['text'])
def FAQ(message):
    if message.text[0] != "/":
        bot.send_message(message.chat.id, "Для получения фото нажмите /dogs", reply_markup=reply())


bot.polling()
