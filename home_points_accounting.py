import telebot
import json
import datetime
import numbers
from bot import Bot
        

class BotDecorator(Bot):
    """docstring for Bot"""

    def __init__(self):
        super(BotDecorator, self).__init__()
        self._id = 0
        self._callback_separator = "_"
        self._keyboards = {}
        self._actions_poins = {}
        self.read_settings()

    def read_settings(self):
        with open("Settings/settings.json", encoding='utf-8') as settings:
            data = json.load(settings)
            self._people_id_name = {
                int(i): name for i, name in data["people_id_name"].items()}
        with open("Settings/actions.json", encoding='utf-8') as settings:
            self._actions = json.load(settings)
            self._create_menus()
        with open("Settings/points.json", encoding='utf-8') as points:
            data = json.load(points)
            self._points = {
                int(i): int(points) for i, points in data.items()}

    def _create_menus(self):
        keyboard = self._create_additional_menu(self._actions)
        keyboard.add(telebot.types.InlineKeyboardButton(text="Баланс",
                                                        callback_data="balance"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="Обнулить",
                                                        callback_data="to_zero"))
        self._main_keyboard = keyboard

    def _create_additional_menu(self, values_dict):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for key in values_dict.keys():
            if isinstance(values_dict[key], dict):
                new_keyboard = self._create_additional_menu(values_dict[key])
                callback = "keyboard" + self._callback_separator + str(len(self._keyboards))
                self._keyboards[callback] = new_keyboard
            elif isinstance(values_dict[key], numbers.Number):
                callback = "action" + self._callback_separator + str(len(self._actions_poins))
                self._actions_poins[callback] = int(values_dict[key])
            keyboard.add(telebot.types.InlineKeyboardButton(text=key,
                                                            callback_data=callback))
        return keyboard

    def get_text_messages(self, message):
        if message.from_user.id in self._people_id_name:
            self._bot.send_message(message.from_user.id,
                                   text="Хаюшки, выбирай\U0001F60A",
                                   reply_markup=self._main_keyboard)
        else:
            self._bot.send_message(call.message.chat.id,
                                   text="Не для тебя моя роза цвела")

    def callback_worker(self, call):
        if call.message.chat.id in self._people_id_name:
            data = call.data
            if data in self._keyboards:
                self._bot.send_message(call.message.chat.id,
                                        text="Выбирай",
                                        reply_markup=self._keyboards[data])               
            elif data in self._actions_poins:
                user = call.message.chat.id
                self._points[user] += self._actions_poins[data]
                message = f"Умничка, тебе начислено {self._actions_poins[data]} баллов.\nТекущий баланс:{self._points[user]}"
                self._bot.send_message( user,
                                        text=message,
                                        reply_markup=self._main_keyboard)
                self.save_points()
            elif call.data == "balance":
                 self._bot.send_message(call.message.chat.id,
                                        text=self.get_balance())               
            elif call.data == "to_zero":
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="Обнулить",
                                                                callback_data="to_zero_approval"))
                self._bot.send_message(call.message.chat.id, text="Вы уверены?", reply_markup=keyboard)
            elif call.data == "to_zero_approval":
                self.set_points_to_zero()
                self._bot.send_message(call.message.chat.id, text="Готово")

    def save_points(self):
        with open("Settings/points.json", 'w') as points:
            json.dump(self._points, points)

    def get_balance(self):
        balance = ""
        for user in self._people_id_name.keys():
            balance += f"{self._people_id_name[user]}: {self._points[user]} баллов.\n"
        return balance

    def set_points_to_zero(self):
        for key in self._points.keys():
            self._points[key] = 0;
        self.save_points()
