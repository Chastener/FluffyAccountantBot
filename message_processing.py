from Telegram_bot import BotDecorator
from cost_accounting import CostAccounting
from bot import Bot
import json


class MessageHandler(Bot):
    """Message processing"""

    def __init__(self):
        with open("Settings/settings.json") as settings:
            data = json.load(settings)
            self._key = data["key"]
        self._cost_accounting = CostAccounting()
        self._bot_decorator = BotDecorator()

    def set_bot(self, bot):
        super(MessageHandler, self).set_bot(bot)
        self._bot_decorator.set_bot(bot)
        self._cost_accounting.set_bot(bot)

    def get_bot_key(self):
        return self._key

    def process_message(self, message):
        try:
            float(message.html_text)
            self._cost_accounting.get_text_messages(message)
        except:
            self._bot_decorator.get_text_messages(message)

    def process_callback(self, call):
        data = call.data.split("_")
        if call.data == "expenses_balance":
            self._cost_accounting.get_balance(call)
        elif call.data == "expenses_to_zero":
            self._cost_accounting.to_zero()
        elif data[0] == "expenses":
            self._cost_accounting.callback_worker(call)
        else:
            self._bot_decorator.callback_worker(call)
