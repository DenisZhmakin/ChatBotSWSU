from abc import ABC, abstractmethod


class AbstractBot(ABC):
    @abstractmethod
    def handle_idiom(self, message):
        pass

    @abstractmethod
    def handle_abbreviations(self, message):
        pass

    @abstractmethod
    def handle_translate(self, message):
        pass

    @abstractmethod
    def route_messages(self, message):
        pass

    @abstractmethod
    def send_keyboard(self, user_id, message, keyboard):
        pass

    @abstractmethod
    def send_reply(self, user_id, message):
        pass

    @abstractmethod
    def run(self):
        pass
