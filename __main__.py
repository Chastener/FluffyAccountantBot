from Telegram_bot import BotDecorator
import telebot

if __name__ == '__main__':
    helper = BotDecorator()
    bot = telebot.TeleBot(helper.get_bot_key())
    helper.set_bot(bot)

    @bot.message_handler(content_types=["text"])
    def get_text_messages(message):
        helper.get_text_messages(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        helper.callback_worker(call)

    bot.polling(none_stop=True, interval=0)
