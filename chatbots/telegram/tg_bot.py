import telebot

from chatbots.telegram.keyboard import TgKeyBoard


class TelegramBot:
    def __init__(self, token: str):
        self.tg_bot = telebot.TeleBot(token=token)
        self.tg_bot.message_handler()(self.message_handler)

    def message_handler(self, message):
        if message.text == "/start" or message.text == "Начать":
            keyboard = TgKeyBoard.get_standard_keyboard()
            self.tg_bot.send_message(message.chat.id, "Добро пожаловать!!!", reply_markup=keyboard)
        elif message.text == "Завершить работу":
            keyboard = TgKeyBoard.get_initial_keyboard()
            self.tg_bot.send_message(message.chat.id, "До свидания!!!", reply_markup=keyboard)

    def run_bot(self):
        self.tg_bot.infinity_polling()
