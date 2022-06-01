from googletrans import Translator

from backend.exceptions.lang_exception import LanguageSupportNotImplementedException
from backend.search_engine import SearchEngine
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
        if self.action_dictionary_status:
            engine = SearchEngine()
            result = engine.find_abbreviations(message.text)
            self.send_message(message.chat.id, result)
            self.action_dictionary_status = False
            return

        if self.action_translate_status:
            engine = SearchEngine()
            result = engine.get_translate(message.text)
            self.send_message(message.chat.id, result)
            self.action_translate_status = False
            return

        if message.text == "/start" or message.text == "Начать":
            keyboard = TgKeyBoard.get_standard_keyboard()

            self.set_keyboard(
                message.chat.id,
                "Добро пожаловать!!!",
                keyboard
            )
        elif message.text == "Поиск по идиомам":
            if not self.action_dictionary_status:
                self.send_message(message.chat.id, "Введите то, что хотите найти в словаре")
                self.action_dictionary_status = True
        elif message.text == "Перевести текст":
            if not self.action_dictionary_status:
                self.send_message(message.chat.id, "Введите то, что хотите перевести")
                self.action_translate_status = True
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
