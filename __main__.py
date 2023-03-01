from message_processing import MessageHandler
import telebot

if __name__ == '__main__':
    message_handler = MessageHandler()
    bot = telebot.TeleBot(message_handler.get_bot_key()) #создали бота с помощью ключа,cоздали объект класса telebot
    message_handler.set_bot(bot)

    @bot.message_handler(content_types=["text"])
    def get_text_messages(message):
        message_handler.process_message(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        message_handler.process_callback(call)

    bot.polling(none_stop=True, interval=0)
