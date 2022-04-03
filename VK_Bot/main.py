import vk_api
from googletrans import Translator
from vk_api.longpoll import VkLongPoll, VkEventType

from config import MY_TOKEN


def _main():
    session = vk_api.VkApi(token=MY_TOKEN)
    translator = Translator()

    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            text = event.text

            session.method("messages.send", {
                "user_id": user_id,
                "message": translator.translate(text, dest='en').text,
                "random_id": 0
            })


if __name__ == '__main__':
    _main()
