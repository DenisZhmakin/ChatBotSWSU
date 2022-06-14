from telebot import types

from backend.search_engine import SearchEngine
from chatbots.common.abs_bot import AbstractBot
from chatbots.common.abs_keyboard import AbstractKeyboard


class TgKeyBoard(AbstractKeyboard):
    @staticmethod
    def get_standard_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        keyboard.add(
            types.KeyboardButton('Поиск по идиомам'),
            types.KeyboardButton('Поиск по аббревиатурам'),
            types.KeyboardButton('Перевести текст'),
            types.KeyboardButton('Поиск в словаре'),
            types.KeyboardButton('Завершить работу')
        )

        return keyboard

    @staticmethod
    def get_initial_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(types.KeyboardButton("Начать"))
        return keyboard

    @staticmethod
    def get_dictionary_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(types.KeyboardButton("Информация о существительном"))
        keyboard.add(types.KeyboardButton("Информация о глаголе"))
        keyboard.add(types.KeyboardButton("Информация о прилагательном"))

        return keyboard

    @staticmethod
    def get_mode_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(types.KeyboardButton("Назад"))
        return keyboard


class TelegramBot(AbstractBot):
    def __init__(self, token: str):
        import telebot
        self.tg_bot = telebot.TeleBot(token=token)
        self.tg_bot.message_handler()(self.route_messages)
        self.engine = SearchEngine()
        self.working_mode = None

    def handle_idiom(self, message):
        result = self.engine.find_idiom(message.text)
        self.send_reply(message.chat.id, result)

    def handle_abbreviations(self, message):
        result = self.engine.find_abbreviations(message.text)
        self.send_reply(message.chat.id, result)

    def handle_info_nouns(self, message):
        result = ""
        word = SearchEngine.get_word_info(message.text)

        if word.speech_part == "существительное":
            result += f"Тип речи: {word.speech_part}\n\n"
            result += f"Перевод: {','.join(word.translates)}\n\n"
            result += "Связанные слова\n\n"
            result += f"Синонимы: {','.join(word.synonyms)}\n"
            result += f"Антонимы: {','.join(word.antonyms)}\n"
            result += f"Родственные слова: {','.join(word.related_words)}\n"
        else:
            result = "Переданное слово не существительное"

        self.send_reply(message.chat.id, result)

    def handle_info_verbs(self, message):
        result = ""
        word = SearchEngine.get_word_info(message.text)

        if word.speech_part == "глагол":
            result += f"Тип речи: {word.speech_part}\n\n"
            result += f"Перевод: {','.join(word.translates)}\n\n"
            result += "Связанные слова\n\n"
            result += f"Синонимы: {','.join(word.synonyms)}\n"
            result += f"Антонимы: {','.join(word.antonyms)}\n"
            result += f"Родственные слова: {','.join(word.related_words)}\n"
        else:
            result = "Переданное слово не глагол"

        self.send_reply(message.chat.id, result)

    def handle_info_adjective(self, message):
        result = ""
        word = SearchEngine.get_word_info(message.text)

        if word.speech_part == "прилагательное":
            result += f"Тип речи: {word.speech_part}\n\n"
            result += f"Перевод: {','.join(word.translates[:6])}\n\n"
            result += "Связанные слова\n\n"
            result += f"Синонимы: {','.join(word.synonyms[:6])}\n"
            result += f"Антонимы: {','.join(word.antonyms[:6])}\n"
            result += f"Родственные слова: {','.join(word.related_words[:6])}\n"
        else:
            result = "Переданное слово не прилагательное"

        self.send_reply(message.chat.id, result)

    def handle_translate(self, message):
        result = self.engine.get_translate(message.text)
        self.send_reply(message.chat.id, result)

    def route_messages(self, message):
        if message.text == "/start" or message.text == "Начать":
            keyboard = TgKeyBoard.get_standard_keyboard()
            self.send_keyboard(message.chat.id, "Добро пожаловать.", keyboard)
        if message.text == "Назад":
            keyboard = TgKeyBoard.get_standard_keyboard()
            self.send_keyboard(message.chat.id, "Выход в главное меню", keyboard)
            self.working_mode = None
        elif message.text == "Поиск по идиомам":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Режим поиска по идиомам", keyboard)
            self.working_mode = "idiom_mode"
        elif message.text == "Поиск по аббревиатурам":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Режим поиска по аббревиатурам", keyboard)
            self.working_mode = "abbreviations_mode"
        elif message.text == "Поиск в словаре":
            keyboard = TgKeyBoard.get_dictionary_keyboard()
            self.send_keyboard(message.chat.id, "Режим поиска в словаре", keyboard)
        elif message.text == "Информация о существительном":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Режим получения информации о существительном", keyboard)
            self.working_mode = "nouns_info_mode"
        elif message.text == "Информация о глаголе":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Режим получения информации о глаголе", keyboard)
            self.working_mode = "verbs_info_mode"
        elif message.text == "Информация о прилагательном":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Режим получения информации о прилагательном", keyboard)
            self.working_mode = "adjective_info_mode"
        elif message.text == "Перевести текст":
            keyboard = TgKeyBoard.get_mode_keyboard()
            self.send_keyboard(message.chat.id, "Введите то, что хотите перевести", keyboard)
            self.working_mode = "translate_mode"
        elif message.text == "Завершить работу":
            keyboard = TgKeyBoard.get_initial_keyboard()
            self.send_keyboard(message.from_id, "До скорой встречи.", keyboard)
        else:
            if self.working_mode == "idiom_mode":
                self.handle_idiom(message)
            elif self.working_mode == "abbreviations_mode":
                self.handle_abbreviations(message)
            elif self.working_mode == "nouns_info_mode":
                self.handle_info_nouns(message)
            elif self.working_mode == "verbs_info_mode":
                self.handle_info_verbs(message)
            elif self.working_mode == "adjective_info_mode":
                self.handle_info_adjective(message)
            elif self.working_mode == "translate_mode":
                self.handle_translate(message)

    def send_keyboard(self, user_id, message, keyboard):
        self.tg_bot.send_message(user_id, message, reply_markup=keyboard)

    def send_reply(self, user_id, message):
        self.tg_bot.send_message(user_id, message)

    def run(self):
        self.tg_bot.infinity_polling()