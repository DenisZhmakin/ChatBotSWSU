from googletrans import Translator

from chatbots.telegram.keyboard import TgKeyBoard


class TelegramBot:
    def __init__(self, token: str):
        import telebot
        self.tg_bot = telebot.TeleBot(token=token)
        self.tg_bot.message_handler()(self.message_handler)

        self.action_dictionary_status = False
        self.action_translate_status = False

        self.translator = Translator()

    def set_keyboard(self, chat_id, text, keyboard):
        self.tg_bot.send_message(chat_id, text, reply_markup=keyboard)

    def message_handler(self, message):
        if message.text == "/start" or message.text == "Начать":
            keyboard = TgKeyBoard.get_standard_keyboard()

            self.set_keyboard(
                message.chat.id,
                "Добро пожаловать!!!",
                keyboard
            )
        elif message.text == "Подобрать синоним":
            if not self.action_dictionary_status:
                self.send_message(message.chat.id, "Введите то, что хотите найти в словаре")
                self.action_dictionary_status = True
        elif message.text == "Перевести текст":
            if not self.action_dictionary_status:
                self.send_message(message.chat.id, "Введите то, что хотите перевести")
                self.action_translate_status = True
        elif self.action_dictionary_status:
            self.send_message(message.chat.id, message.text)
            self.action_dictionary_status = False
        elif self.action_translate_status:
            text = self.translator.translate(message.text, dest='en').text
            self.send_message(message.chat.id, text)
            self.action_translate_status = False
        elif message.text == "Завершить работу":
            keyboard = TgKeyBoard.get_initial_keyboard()

            self.set_keyboard(
                message.chat.id,
                "До свидания.",
                keyboard
            )

    def send_message(self, chat_id, text):
        self.tg_bot.send_message(chat_id, text)

    def run_bot(self):
        self.tg_bot.infinity_polling()
