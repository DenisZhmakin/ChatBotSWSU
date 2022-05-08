import os
from dotenv import load_dotenv

from chatbots.telegram import TelegramBot
from chatbots.vkontakte import VkontakteBot


def _main():
    load_dotenv()

    # vkbot = VkontakteBot(os.getenv("VK_TOKEN"))
    tgbot = TelegramBot(os.getenv("TG_TOKEN"))

    # vkbot.run_bot()
    tgbot.run_bot()


if __name__ == '__main__':
    _main()
