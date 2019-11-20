import configparser
import requests
import telebot
from telebot import apihelper
from bs4 import BeautifulSoup
import datetime
import calendar

config = configparser.ConfigParser()
config.read('config.ini')
cfg = config['data']
bot = telebot.TeleBot(cfg['access_token'])
apihelper.proxy = {'https':'https://141.125.82.106:80'}

days = {
    'monday': '1day',
    'tuesday': '2day',
    'wednesday': '3day',
    'thursday': '4day',
    'friday': '5day',
    'saturday': '6day',
    'sunday': '7day',
    '1day': 'monday',
    '2day': 'tuesday',
    '3day': 'wednesday',
    '4day': 'thursday',
    '5day': 'friday',
    '6day': 'saturday',
    '7day': 'sunday'
    }

days2 = {
    'monday': 'Пн',
    'tuesday': 'Вт',
    'wednesday': 'Ср',
    'thursday': 'Чт',
    'friday': 'Пт',
    'saturday': 'Сб',
    'sunday': 'Вс'
    }


def get_page(group, week=''):

    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=cfg['domain'],
        week=week,
        group=group)

    response = requests.get(url)
    web_page = response.text

    return web_page


def parse_schedule(web_page, day):

    soup = BeautifulSoup(web_page, 'html5lib')

    schedule_table = soup.find('table', attrs={'id': days[day]})

    times_list = schedule_table.find_all('td', attrs={'class': 'time'})
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all(
        'td', attrs={'class': 'room'}
    )
    locations_list = [room.span.text for room in locations_list]

    lessons_list = schedule_table.find_all(
        'td', attrs={'class': 'lesson'}
    )
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info])
                    for lesson_info in lessons_list
                    ]

    classrooms_list = schedule_table.find_all(
        'dd', attrs={'class': 'rasp_aud_mobile'}
    )
    classrooms_list = [classroom.text for classroom in classrooms_list]

    return times_list, locations_list, lessons_list, classrooms_list


@bot.message_handler(commands=[
    'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):

    x = message.text.split()
    if len(x) == 2:
        day, group = message.text.split()
        web_page = get_page(group)
    elif len(x) == 3:
        day, group, week = message.text.split()
        web_page = get_page(group, week)

    if 'Расписание не найдено' in web_page:
        bot.send_message(message.chat.id, 'Такой группы нет')

    else:
        try:
            day = str(day[1:])
            times_lst, locations_lst, lessons_lst, classrooms_lst = \
                parse_schedule(web_page, day)
            resp = ''
            for time, location, lesson, room in zip(
                times_lst, locations_lst, lessons_lst, classrooms_lst
            ):
                resp += '<b>{}</b>\n<b>{}</b>\n \
                {}\n{}\n{}\n\n'.format(
                    days2[day], time, location, lesson, room
                )
            bot.send_message(message.chat.id, resp, parse_mode='HTML')

        except AttributeError:
            resp = 'Занятий нет, уточни в ИСУ'
            bot.send_message(message.chat.id, resp)


@bot.message_handler(commands=['near'])
def get_near_lesson(message):

    curr_datetime = datetime.datetime.now().isoformat(timespec='minutes')
    now = datetime.datetime.now()
    curr_time = curr_datetime[11:17]
    weekday = calendar.weekday(
        int(curr_datetime[:4]),
        int(curr_datetime[5:7]),
        int(curr_datetime[8:10])
    )
    weekday += 1
    weekday = str(weekday)

    _, group = message.text.split()
    web_page = get_page(group)
    if 'Расписание не найдено' in web_page:
        bot.send_message(message.chat.id, 'Такой группы нет')
    else:

        # if study today
        try:
            day = days[weekday + 'day']
            times_lst, locations_lst, lessons_lst, classrooms_lst = \
                parse_schedule(web_page, day)

            first = times_lst[0]
            hour1 = int(first[:2])
            min1 = int(first[4:5])
            first = now.replace(hour=hour1, minute=min1,
                                second=0, microsecond=0
                                )
            last = times_lst[-1]
            hour1 = int(last[:2])
            min1 = int(last[4:5])
            last = now.replace(hour=hour1, minute=min1,
                               second=0, microsecond=0
                               )
            if now < first:
                resp = ''
                resp += '<b>{}</b>\n<b>{}</b>\n \
                {}\n{}\n{}\n\n'.format(
                    day2[day], times_lst[0], locations_lst[0],
                    lessons_lst[0], classrooms_lst[0]
                )
                bot.send_message(message.chat.id, resp, parse_mode='HTML')

            elif first <= now < last:
                for i in range(1, len(times_lst)):
                    num += 1
                    time = times_lst[i]
                    hour1 = int(time[:2])
                    min1 = int(time[4:5])
                    curr_lesson = now.replace(hour=hour1, minute=min1,
                                              second=0, microsecond=0
                                              )
                    if now < curr_lesson:
                        resp = ''
                        resp += '<b>{}</b>\n<b>{}</b>\n \
                        {}\n{}\n{}\n\n'.format(
                            days2[day], times_lst[num], locations_lst[num],
                            lessons_lst[num], classrooms_lst[num]
                        )
                        bot.send_message(message.chat.id, resp,
                                         parse_mode='HTML'
                                         )
                    else:
                        num += 1
                        continue

            elif now >= last:
                for _ in range(1, 7):
                    if weekday == 7:
                        weekday = 0
                        continue
                    weekday = int(weekday) + 1
                    day = days[str(weekday) + 'day']
                    try:
                        times_lst, locations_lst, lessons_lst,
                        classrooms_lst = parse_schedule(web_page, day)
                        resp = ''
                        resp += '<b>{}</b>\n<b>{}</b>\n \
                        {}\n{}\n{}\n\n'.format(
                            days2[day], times_lst[0], locations_lst[0],
                            lessons_lst[0], classrooms_lst[0]
                            )
                        bot.send_message(message.chat.id, resp,
                                         parse_mode='HTML'
                                         )
                        break
                    except AttributeError:
                        continue

    # if no lessons today
        except AttributeError:
            for _ in range(1, 7):
                if weekday == 7:
                    weekday = 0
                    continue
                weekday = int(weekday) + 1
                day = days[str(weekday) + 'day']
                try:
                    times_lst, locations_lst, lessons_lst, classrooms_lst = \
                        parse_schedule(web_page, day)
                    resp = ''
                    resp += '<b>{}</b>\n<b>{}</b>\n \
                    {}\n{}\n{}\n\n'.format(
                        days2[day], times_lst[0], locations_lst[0],
                        lessons_lst[0], classrooms_lst[0]
                    )
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    break

                except AttributeError:
                    continue


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):

    x = message.text.split()
    if len(x) == 2:
        _, group = message.text.split()
        web_page = get_page(group)
    elif len(x) == 3:
        _, group, week = message.text.split()
        web_page = get_page(group, week)

    if 'Расписание не найдено' in web_page:
        bot.send_message(message.chat.id, 'Такой группы нет')

    else:
        curr_datetime = datetime.datetime.now().isoformat()
        weekday = calendar.weekday(
            int(curr_datetime[:4]),
            int(curr_datetime[5:7]),
            int(curr_datetime[8:10])
        )
        weekday += 2
        weekday = str(weekday)
        day = days[weekday + 'day']

        try:
            times_lst, locations_lst, lessons_lst, classrooms_lst = \
                parse_schedule(web_page, day)
            resp = ''
            for time, location, lesson, room in zip(
                    times_lst, locations_lst, lessons_lst, classrooms_lst):
                resp += '<b>{}</b>\n<b>{}</b>\n \
                {}\n{}\n{}\n\n'.format(
                    days2[day], time,
                    location, lesson, room
                )
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            resp = 'Завтра занятий нет. На всякий случай уточни в ИСУ'
            bot.send_message(message.chat.id, resp)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):

    x = message.text.split()
    if len(x) == 2:
        _, group = message.text.split()
        web_page = get_page(group)
    elif len(x) == 3:
        _, group, week = message.text.split()
        web_page = get_page(group, week)

    if 'Расписание не найдено' in web_page:
        bot.send_message(message.chat.id, 'Такой группы нет')

    else:
        whole_week = ['monday', 'tuesday', 'wednesday',
                      'thursday', 'friday', 'saturday', 'sunday'
                      ]
        for day in whole_week:
            resp = ''

            try:
                times_lst, locations_lst, lessons_lst, classrooms_lst = \
                    parse_schedule(web_page, day)
                for time, location, lesson, room in zip(
                        times_lst, locations_lst, lessons_lst, classrooms_lst
                ):
                    resp += '<b>{}</b>\n<b>{}</b>\n \
                    {}\n{}\n{}\n\n'.format(
                        days2[day], time, location, lesson, room
                    )
                bot.send_message(message.chat.id, resp, parse_mode='HTML')

            except AttributeError:
                resp = '<b>{}</b>\nЗанятий нет'.format(days2[day])
                bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
