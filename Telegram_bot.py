import telebot
import csv
import json
import datetime
from bot import Bot
#TODO "" everywhere
        

class BotDecorator(Bot):
    """docstring for Bot"""

    def __init__(self):
        super(BotDecorator, self).__init__()
        self._id = 0
        self.read_settings()

    def _create_more_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="Улучшение жизни",
                                                        callback_data="keyboard_work"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="Штрафы",
                                                        callback_data="keyboard_taxes"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="Баланс",
                                                        callback_data="balance"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="Обнулить",
                                                        callback_data="to_zero"))
        self._more_keyboard = keyboard

    def save_points(self):
        with open("Settings/points.json", 'w') as points:
            json.dump(self._points, points)

    def _create_work_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i, key in enumerate(self._actions["Домашние дела"].keys()):
            keyboard.add(telebot.types.InlineKeyboardButton(text=key,
                                                            callback_data=f"work_{i}"))
        self._work_keyboard = keyboard

    def _create_taxes_menu(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i, key in enumerate(self._actions["Штрафы"].keys()):
            keyboard.add(telebot.types.InlineKeyboardButton(text=key,
                                                            callback_data=f"taxes_{i}"))
        self._taxes_keyboard = keyboard

    def read_settings(self):
        with open("Settings/settings.json", encoding='utf-8') as settings:
            data = json.load(settings)
            self._people_id_name = {
                int(i): name for i, name in data["people_id_name"].items()}
        with open("Settings/actions.json", encoding='utf-8') as settings:
            self._actions = json.load(settings)
            print(self._actions)
            self._create_more_menu()
            self._create_work_menu()
            self._create_taxes_menu()
        with open("Settings/points.json", encoding='utf-8') as points:
            data = json.load(points)
            self._points = {
                int(i): int(points) for i, points in data.items()}

    def get_text_messages(self, message):
        if message.from_user.id in self._people_id_name:
            self._bot.send_message(message.from_user.id,
                                   text="Хаюшки, выбирай\U0001F60A",
                                   reply_markup=self._more_keyboard)

        else:
            self._bot.send_message(call.message.chat.id,
                                   text="Не для тебя моя роза цвела")

    def log(self, user, list_name, action_id):
        time = datetime.datetime.now()
        # with open("Settings/log.txt", 'a') as log:
            # log.write(f"{time} {self._people_id_name[user]} {getattr(self, '_' + list_name)[action_id][0]} Цена:{getattr(self, '_' + list_name)[action_id][1]} Баланс:{self._points[user]}\n")

    def get_balance(self):
        balance = ""
        for user in self._people_id_name.keys():
            balance += f"{self._people_id_name[user]}: {self._points[user]} баллов.\n"
        return balance

    def set_points_to_zero(self):
        for key in self._points.keys():
            self._points[key] = 0;
        self.save_points()

    def callback_worker(self, call):
        if call.message.chat.id in self._people_id_name:
            data = call.data.split("_")
            if data[0] == "keyboard":
                self._bot.send_message(call.message.chat.id,
                                       text="Выбирай",
                                       reply_markup=getattr(self, "_" + data[1] + "_keyboard"))
            elif data[0] == "work":
                action = list(self._actions["Домашние дела"].keys())[int(data[1])]
                action_value = self._actions["Домашние дела"][action]
                for user in self._people_id_name.keys():
                    if user != call.message.chat.id:
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Отклонить",
                                                                        callback_data=f"decline_{call.message.chat.id}_{data[1]}"))
                        self._bot.send_message(user,
                                               text=f"{self._people_id_name[call.message.chat.id]} сделал(а) {action}",
                                               reply_markup=keyboard)
                    else:
                        self._points[user] += action_value
                        message = f"Умничка, тебе начислено {action_value} баллов.\nТекущий баланс:{self._points[user]}"
                        self._bot.send_message( user,
                                                text=message,
                                                reply_markup=self._more_keyboard)
                        self.log(user, "work", int(data[1]))
                        self.save_points()
            elif data[0] == "taxes":
                user = call.message.chat.id
                action = list(self._actions["Штрафы"].keys())[int(data[1])]
                action_value = self._actions["Штрафы"][action]
                self._points[user] -= action_value
                message = f"Косяк, косяк... Лови минус {action_value} баллов.\nТекущий баланс:{self._points[user]}"
                self._bot.send_message(user,
                                       text=message,
                                       reply_markup=self._more_keyboard)
                self.save_points()
                self.log(user, "taxes", int(data[1]))
            elif data[0] == "balance":
                self._bot.send_message(call.message.chat.id,
                                       text=self.get_balance(),
                                       reply_markup=self._more_keyboard)
            elif data[0] == "decline":
                action = list(self._actions["Домашние дела"].keys())[int(data[2])]
                action_value = self._actions["Домашние дела"][action]
                self._points[int(data[1])] -= action_value
                self._bot.send_message(int(data[1]),
                                       text=f"{self._people_id_name[call.message.chat.id]} отклонил(а) {action}.\nТекущий баланс:{self._points[int(data[1])]}")
                self.save_points()
            elif call.data == "to_zero":
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="Обнулить",
                                                                callback_data="to_zero_approval"))

                self._bot.send_message(call.message.chat.id, text="Вы уверены?", reply_markup=keyboard)
            elif call.data == "to_zero_approval":
                self.set_points_to_zero()
                self._bot.send_message(call.message.chat.id, text="Готово")
