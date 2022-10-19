from os import getenv

import telebot
from telebot import types


token = getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help")
    bot.send_message(
        message.chat.id,
        "Привет! Хочешь узнать свежую информацию о МТУСИ?",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["help"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Я умею сообщать вам адрес официального сайта МТУСИ\n\n"
        "/help — получить список доступных команд"
    )


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, "Тогда тебе сюда — https://mtuci.ru/")


bot.infinity_polling()
