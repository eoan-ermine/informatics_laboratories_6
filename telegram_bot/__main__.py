from os import getenv

import telebot
from telebot import types
from dotenv import load_dotenv

import psycopg2
import psycopg2.extras


load_dotenv()


token = getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)
conn = psycopg2.connect(
	database=getenv("PG_DATABASE"), user=getenv("PG_USER"), password=getenv("PG_PASSWORD"),
	host=getenv("PG_HOST"), port=getenv("PG_PORT")
)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


MONDAY_MESSAGE, TUESDAY_MESSAGE, WEDNESDAY_MESSAGE = "Понедельник", "Вторник", "Среда"
THURSDAY_MESSAGE, FRIDAY_MESSAGE = "Четверг", "Пятница"
CURRENT_WEEK_MESSAGE, NEXT_WEEK_MESSAGE = "Расписание на текущую неделю", "Расписание на следующую неделю"

WEEKDAY_MAPPING = {
    MONDAY_MESSAGE: 1, TUESDAY_MESSAGE: 2, WEDNESDAY_MESSAGE: 3,
    THURSDAY_MESSAGE: 4, FRIDAY_MESSAGE: 5
}
REVERSE_WEEKDAY_MAPPING = {
    value: key for key, value in WEEKDAY_MAPPING.items()
}


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    
    keyboard.row(MONDAY_MESSAGE, TUESDAY_MESSAGE, WEDNESDAY_MESSAGE)
    keyboard.row(THURSDAY_MESSAGE, FRIDAY_MESSAGE)
    keyboard.row(CURRENT_WEEK_MESSAGE, NEXT_WEEK_MESSAGE)

    bot.send_message(
        message.chat.id,
        "Привет! Хочешь узнать свежую информацию о МТУСИ?",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Я умею сообщать вам адрес официального сайта МТУСИ\n\n"
        "/help — получить список доступных команд\n"
        "/mtuci — получить ссылку на официальный сайт МТУСИ"
    )


@bot.message_handler(commands=["mtuci"])
def mtuci_command(message):
    bot.send_message(
        message.chat.id,
        "Официальный сайт МТУСИ доступен по адресу https://mtuci.ru/"
    )


def retrieve_schedule(weekday: int):
    cursor.execute(
        "SELECT subject.name AS subject, LOWER(class_type.name) AS subject_type, day, room_number, classes_timetable.start_time AS start_time, teacher.full_name AS teacher FROM bot.timetable "
        "INNER JOIN bot.class ON timetable.class = class.id INNER JOIN bot.subject ON class.subject = subject.id INNER JOIN bot.class_type ON class.class_type = class_type.id "
        "INNER JOIN bot.classes_timetable ON timetable.class_number = classes_timetable.id "
        "INNER JOIN bot.teacher_class ON timetable.class = teacher_class.class INNER JOIN bot.teacher ON teacher_class.teacher = teacher.id "
        "WHERE day = %s", (weekday,)
    )
    return [cursor.fetchall()]


def format_schedule(schedule) -> str:
    formatted_day_schedules = []
    for day_schedule in schedule:
        if day_schedule:
            formatted_day_schedules.append(
                f"{REVERSE_WEEKDAY_MAPPING[day_schedule[0]['day']]}\n" +
                "------------------\n" +
                "\n".join([f"{timetable['subject']} ({timetable['subject_type']})\t{timetable['room_number']}\t{timetable['start_time']}\t{timetable['teacher']}" for timetable in day_schedule]) +
                "\n------------------\n"
            )
        else:
            formatted_day_schedules.append("К сожалению, у нас нет расписания на этот день")
    return "\n".join(formatted_day_schedules)


@bot.message_handler(content_types=["text"])
def answer(message):
    text = message.text

    if text in [MONDAY_MESSAGE, TUESDAY_MESSAGE, WEDNESDAY_MESSAGE, THURSDAY_MESSAGE, FRIDAY_MESSAGE]:
        schedule = retrieve_schedule(WEEKDAY_MAPPING[text])
        bot.send_message(message.chat.id, format_schedule(schedule))
    elif text in [CURRENT_WEEK_MESSAGE, NEXT_WEEK_MESSAGE]:
        bot.send_message(message.chat.id, f"{text}")
    else:
        bot.send_message("Извините, я Вас не понял")

bot.infinity_polling()
