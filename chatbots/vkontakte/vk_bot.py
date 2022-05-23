from googletrans import Translator
from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from backend.exceptions.lang_exception import LanguageSupportNotImplementedException
from backend.search_engine import SearchEngine
from chatbots.vkontakte.keyboard import VkKeyBoard


class VkontakteBot:
    def __init__(self, token: str):
        self.vk_session = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk_session, '210776300')

        self.action_dictionary_status = False
        self.action_translate_status = False

        self.translator = Translator()

    def set_keyboard(self, user_id, message, keyboard):
        post = {
            "user_id": user_id,
            "message": message,
            "keyboard": keyboard.get_keyboard(),
            "random_id": 0
        }

        self.vk_session.method("messages.send", post)

    def message_handler(self, message):
        if self.action_dictionary_status:
            engine = SearchEngine()
            result = engine.get_translate(message.text)
            self.send_message(message.from_id, result)
            self.action_dictionary_status = False
            return

        if self.action_translate_status:
            engine = SearchEngine()

            try:
                result = engine.get_translate(message.text)
            except LanguageSupportNotImplementedException as e:
                result = e.message

            self.send_message(message.from_id, result)
            self.action_translate_status = False
            return

        if message.text == "Начать":
            keyboard = VkKeyBoard.get_standard_keyboard()
            self.set_keyboard(
                message.from_id,
                message="Добро пожаловать!",
                keyboard=keyboard
            )
        elif message.text == "Подобрать синоним":
            if not self.action_dictionary_status:
                self.send_message(message.from_id, "Введите то, что хотите найти в словаре")
                self.action_dictionary_status = True
        elif message.text == "Перевести текст":
            if not self.action_dictionary_status:
                self.send_message(message.from_id, "Введите то, что хотите перевести")
                self.action_translate_status = True
        elif message.text == "Завершить работу":
            keyboard = VkKeyBoard.get_initial_keyboard()
            self.set_keyboard(
                message.from_id,
                message="До свидания.",
                keyboard=keyboard
            )

    def send_message(self, user_id, text):
        post = {
            "user_id": user_id,
            "message": text,
            "random_id": 0
        }

        self.vk_session.method("messages.send", post)

    def run_bot(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.message_handler(event.message)
