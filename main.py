#!/usr/bin/env python3
import os
from threading import Thread

from dotenv import load_dotenv

from chatbots.telegram import TelegramBot
from chatbots.vkontakte import VkontakteBot


def _main():
    load_dotenv()

    # vkbot = VkontakteBot(os.getenv("VK_TOKEN"))
    tgbot = TelegramBot(os.getenv("TG_TOKEN"))

    # Thread(target=vkbot.run_bot).start()
    Thread(target=tgbot.run_bot).start()


if __name__ == '__main__':
    _main()
