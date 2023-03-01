from bot import Bot
from cost_category import CostCategory
import telebot
import json


class CostAccounting(Bot):
    """Cost accounting"""

    def __init__(self):
        with open("Settings/categories.json") as categories:
            data = json.load(categories)
            category_lst = []
            for category in data["categories"]:
                category_lst.append(CostCategory(category["name"], category["current_expenses"],
                                                 category["limit_expenses"]))
            self._categories = category_lst

    def get_text_messages(self, message):
        self._create_menu(message)
        self._bot.send_message(message.from_user.id,
                               text="Выбери в какую категорию внести затраты\U0001F60A",
                               reply_markup=self._more_keyboard)

    def _create_menu(self, message):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(len(self._categories)):
            keyboard.add(telebot.types.InlineKeyboardButton(
                text=f"{self._categories[i].name} + {message.html_text}byn",
                callback_data=f"expenses_{self._categories[i].name}_{message.html_text}"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="Текущие расходы",
                                                        callback_data="expenses_balance"))
        self._more_keyboard = keyboard

    def callback_worker(self, call):
        call_data = call.data.split("_")
        categories_balance = ""
        with open("Settings/categories.json") as categories:
            data = json.load(categories)
            for category in data["categories"]:
                if call.data == "expenses_balance":
                    categories_balance += f"{category['name']}:{category['current_expenses']}/{category['limit_expenses']}\n"
                else:
                    if category["name"] == call_data[1]:
                        category["current_expenses"] += float(call_data[2])
                        with open("Settings/categories.json", "w") as outfile:
                            json.dump(data, outfile)
                        self._bot.send_message(call.message.chat.id,
                                               text=f"Вы внесли затраты {call_data[2]} бел рублей в категорию {category['name']}\n"
                                               f"Текущие расходы:{category['current_expenses']}/{category['limit_expenses']}")
            self._bot.send_message(call.message.chat.id, text=categories_balance)
