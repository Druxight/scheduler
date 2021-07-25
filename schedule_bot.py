#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytz
import datetime
import telebot
from telebot import types

# Global variables
StartMessage = """
Бот для швидкого та зручного доступу до розкладу занять групи КІ-31

Автор: 
@druxight
"""

Times = (
    (datetime.time(8, 30), datetime.time(10, 5)),
    (datetime.time(10, 25), datetime.time(12, 0)),
    (datetime.time(12, 20), datetime.time(13, 55)),
    (datetime.time(14, 15), datetime.time(15, 50)),
    (datetime.time(16, 10), datetime.time(17, 45))
)

with open('schedule.json', 'r', 215, 'utf-8') as file:
    Schedule = json.load(file)

Weekdays = list(Schedule.keys())

client = telebot.TeleBot('1920642321:AAEiMfOWRGRzm5unoEUXfk88SUjX0OJRzCk')


# Methods
def get_lessons_status(time, times):
    status = []
    for i in range(len(times)):
        if times[i][0] <= time <= times[i][1]:
            status.append('\N{black rightwards arrow}')  # '->'
        elif time > times[i][1]:
            status.append('\N{white heavy check mark}')  # '+'
        elif time < times[i][0]:
            status.append('\N{white medium small square}')  # '-'
        else:
            status.append('')
    return status


def get_days_status(day_i, weekdays):
    status = {}
    for i, weekday in enumerate(weekdays):
        if i == day_i:
            status[weekday] = '\N{black rightwards arrow}'  # '->'
        elif i > day_i:
            status[weekday] = '\N{white medium small square}'  # '-'
        elif i < day_i:
            status[weekday] = '\N{white heavy check mark}'  # '+'
        else:
            status[weekday] = ''
    return status


def getMarkupButtons():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    todayMarkup = types.KeyboardButton('Сьогодні')
    tomorrowMarkup = types.KeyboardButton('Завтра')
    weekMarkup = types.KeyboardButton('Тиждень')
    nextWeekMarkup = types.KeyboardButton('Наступний тиждень')
    markup.add(todayMarkup, tomorrowMarkup, weekMarkup, nextWeekMarkup)
    return markup

@client.message_handler(commands=['start'])
def start(income):
    chat_id = income.chat.id
    client.send_message(chat_id, StartMessage, reply_markup=getMarkupButtons())


@client.message_handler(commands=['today'])
def today(income):
    chat_id = income.chat.id

    tzkiev = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tzkiev)
    year, week_num, day_num = datetime.datetime.isocalendar(today)
    time = datetime.datetime.time(today)
    week_num = '1' if week_num % 2 == 0 else '2'

    if day_num <= len(Weekdays):
        day = Weekdays[day_num - 1]
        lessons_status = get_lessons_status(time, Times)
        message = 'Розклад на сьогодні ({}, навчання по {}):\nЗараз: {}\n'.format(
            day, 'чисельнику' if week_num == '1' else 'знаменнику', today.strftime("%d.%m.%Y %H:%M")
        )
        for i in range(len(Times)):
            lesson_num = str(i + 1)
            lesson = Schedule[day][lesson_num][week_num]
            if lesson != '':
                message += '\n{} {}. ({} - {})\n'.format(lessons_status[i], lesson_num,
                                                         Times[i][0].strftime("%H:%M"),
                                                         Times[i][1].strftime("%H:%M"))
                for key in lesson.keys():
                    message += '{}: {}\n'.format(key, lesson[key])
            else:
                message += '\n{} {}. ({} - {})\nПари немає.\n'.format(lessons_status[i], lesson_num,
                                                                      Times[i][0].strftime("%H:%M"),
                                                                      Times[i][1].strftime("%H:%M"))
        client.send_message(chat_id, message)
    else:
        client.send_message(chat_id, 'Занять немає.')


@client.message_handler(commands=['tomorrow'])
def tomorrow(income):
    chat_id = income.chat.id

    tzkiev = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tzkiev)
    year, week_num, day_num = datetime.datetime.isocalendar(today)
    if day_num == 7:
        day_num = 1
        week_num += 1
    else:
        day_num += 1
    week_num = '1' if week_num % 2 == 0 else '2'

    if day_num <= len(Weekdays):
        day = Weekdays[day_num - 1]
        message = 'Розклад на завтра ({}, навчання по {}):\nЗараз: {}\n'.format(
            day, 'чисельнику' if week_num == '1' else 'знаменнику', today.strftime("%d.%m.%Y %H:%M")
        )
        for i in range(len(Times)):
            lesson_num = str(i + 1)
            lesson = Schedule[day][lesson_num][week_num]
            if lesson != '':
                message += '\n{}. ({} - {})\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                      Times[i][1].strftime("%H:%M"))
                for key in lesson.keys():
                    message += '{}: {}\n'.format(key, lesson[key])
            else:
                message += '\n{}. ({} - {})\nПари немає.\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                                   Times[i][1].strftime("%H:%M"))

        client.send_message(chat_id, message)
    else:
        client.send_message(chat_id, 'Занять немає.')


@client.message_handler(commands=['week'])
def week(income):
    chat_id = income.chat.id

    tzkiev = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tzkiev)
    year, week_num, day_num = datetime.datetime.isocalendar(today)
    week_num = '1' if week_num % 2 == 0 else '2'

    days_status = get_days_status(day_num - 1, Weekdays)
    message = 'Розклад на тиждень (навчання по {}):\nЗараз: {}'.format(
        'чисельнику' if week_num == '1' else 'знаменнику', today.strftime("%d.%m.%Y %H:%M")
    )
    for day in Weekdays:
        message += '\n\n{} {}\n'.format(days_status[day], day)
        for i in range(len(Times)):
            lesson_num = str(i + 1)
            lesson = Schedule[day][lesson_num][week_num]
            if lesson != '':
                message += '\n{}. ({} - {})\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                      Times[i][1].strftime("%H:%M"))
                for key in lesson.keys():
                    message += '{}: {}\n'.format(key, lesson[key])
            else:
                message += '\n{}. ({} - {})\nПари немає.\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                                   Times[i][1].strftime("%H:%M"))
    if len(Weekdays) != 0:
        client.send_message(chat_id, message)
    else:
        client.send_message(chat_id, 'Занять немає.')


@client.message_handler(commands=['next_week'])
def next_week(income):
    chat_id = income.chat.id

    tzkiev = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tzkiev)
    year, week_num, day_num = datetime.datetime.isocalendar(today)
    week_num += 1
    week_num = '1' if week_num % 2 == 0 else '2'

    message = 'Розклад на наступний тиждень (навчання по {}):\nЗараз: {}'.format(
        'чисельнику' if week_num == '1' else 'знаменнику', today.strftime("%d.%m.%Y %H:%M")
    )
    for day in Weekdays:
        message += '\n\n{}\n'.format(day)
        for i in range(len(Times)):
            lesson_num = str(i + 1)
            lesson = Schedule[day][lesson_num][week_num]
            if lesson != '':
                message += '\n{}. ({} - {})\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                      Times[i][1].strftime("%H:%M"))
                for key in lesson.keys():
                    message += '{}: {}\n'.format(key, lesson[key])
            else:
                message += '\n{}. ({} - {})\nПари немає.\n'.format(lesson_num, Times[i][0].strftime("%H:%M"),
                                                                   Times[i][1].strftime("%H:%M"))
    if len(Weekdays) != 0:
        client.send_message(chat_id, message)
    else:
        client.send_message(chat_id, 'На наступному тижні занять немає.')


@client.message_handler(content_types=['text'])
def replyer(message):
    if message.text == 'Сьогодні':
        today(message)
    elif message.text == 'Завтра':
        tomorrow(message)
    elif message.text == 'Тиждень':
        week(message)
    elif message.text == 'Наступний тиждень':
        next_week(message)
    else:

        client.send_message(message.chat.id, 'Команду не знайдено', reply_markup=getMarkupButtons())


client.polling(none_stop=True, timeout=0)
