from telebot import types


class TgKeyBoard:
    @staticmethod
    def get_standard_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        keyboard.add(
            types.KeyboardButton('Поиск по идиомам'),
            types.KeyboardButton('Перевести текст'),
            types.KeyboardButton('Завершить работу')
        )

        return keyboard

    @staticmethod
    def get_initial_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        keyboard.add(
            types.KeyboardButton("Начать")
        )

        return keyboard
