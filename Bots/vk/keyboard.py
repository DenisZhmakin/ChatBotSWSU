from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class VkKeyBoard:
    @staticmethod
    def get_standard_keyboard():
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button("Подобрать перевод", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Перевести текст", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Завершить работу", color=VkKeyboardColor.NEGATIVE)

        return keyboard

    @staticmethod
    def get_initial_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Начать", color=VkKeyboardColor.PRIMARY)

        return keyboard
