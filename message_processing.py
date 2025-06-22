from home_points_accounting import BotDecorator
from cost_accounting import CostAccounting
from reminder import Reminder
from bot import Bot
import json


class MessageHandler(Bot):
    """Message processing"""

    def __init__(self):
        with open("Settings/settings.json") as settings:
            data = json.load(settings)
            self._key = data["key"]
        self._reminder = Reminder()

    def set_bot(self, bot):
        super(MessageHandler, self).set_bot(bot)
        self._reminder.set_bot(bot)

    def get_bot_key(self):
        return self._key

    def process_message(self, message):
        self._reminder.process_message(message)

    def process_callback(self, call):
        self._reminder.process_callback(call)
