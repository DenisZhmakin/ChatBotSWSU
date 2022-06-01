from abc import ABC, abstractmethod


class AbstractKeyboard(ABC):
    @staticmethod
    @abstractmethod
    def get_standard_keyboard():
        pass

    @staticmethod
    @abstractmethod
    def get_initial_keyboard():
        pass

    @staticmethod
    @abstractmethod
    def get_mode_keyboard():
        pass
