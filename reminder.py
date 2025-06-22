import telebot
import json
import datetime
import numbers
from bot import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import pytz

class Reminder(Bot):
    """docstring for Bot"""

    def __init__(self):
        super(Reminder, self).__init__()
        self._scheduler = BackgroundScheduler(timezone=pytz.utc)
        self._scheduler.start()

    def process_message(self, message):
        if message.text.startswith("/remindeveryday"):
            self.remind_every_day(message)
        elif message.text.startswith("/remindeveryweek"):
            self.remind_every_day(message)
        else:
            self._bot.reply_to(message, "нужно ввести команду")

    def process_callback(self, call):
        pass

    def remind_every_day(self, message):
        try:
            parts = message.text.split()
            time_part = parts[1]
            hour, minute = map(int, time_part.split(":"))
            text = ' '.join(parts[2:])
            self._scheduler.add_job(
                self.send_reminder,
                trigger=CronTrigger(hour=hour, minute=minute, timezone=pytz.timezone("Europe/Moscow")),
                args=[message.chat.id, text]
            )
            self._bot.reply_to(message, f"✅ Ежедневное напоминание в {time_part}: {text}")
        except Exception as e:
            print(e)
            self._bot.reply_to(message, "⚠ Пример: /remindeveryday 08:00 Пить воду")

    def remind_every_week(self, message):
        try:
            parts = message.text.split()
            weekday_map = {
                'понедельник': 'mon', 'вторник': 'tue', 'среда': 'wed',
                'четверг': 'thu', 'пятница': 'fri', 'суббота': 'sat', 'воскресенье': 'sun'
            }
            weekday_rus = parts[1].lower()
            weekday = weekday_map.get(weekday_rus)
            if not weekday:
                raise ValueError("Неверный день недели")
            hour, minute = map(int, parts[2].split(":"))
            text = ' '.join(parts[3:])
            self._scheduler.add_job(
                self.send_reminder,
                trigger=CronTrigger(day_of_week=weekday, hour=hour, minute=minute, timezone=pytz.timezone("Europe/Moscow")),
                args=[message.chat.id, text]
            )
            self._bot.reply_to(message, f"✅ Еженедельное напоминание: {weekday_rus.capitalize()} в {parts[2]} — {text}")
        except:
            self._bot.reply_to(message, "⚠ Пример: /remindeveryweek понедельник 09:00 Встреча с командой")

    def send_reminder(self, chat_id, text):
        self._bot.send_message(chat_id, f"🔔 Напоминание: {text}")