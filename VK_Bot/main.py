import vk_api
from googletrans import Translator
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import MY_TOKEN
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# if event.message.fwd_messages:
#     # fwd_messages = event.message.fwd_messages
#     #
#     # for message in fwd_messages:
#     #     while 'fwd_messages' in message:
#     #         message = message['fwd_messages']
#     #     else:
#     #         if 'fwd_messages' in message:
#     #             while message['fwd_messages']:
#     #                 pass
#     #         else:
#     #             send_message(vk_session, event.message.from_id, message['text'])
#     pass
# else:
#     send_message(vk_session, event.message.from_id, event.message.text)


def send_message(session, user_id, text, keyboard=None):
    translator = Translator()

    post = {
        "user_id": user_id,
        "message": translator.translate(text, dest='ru').text,
        "random_id": 0
    }

    if keyboard is not None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    session.method("messages.send", post)


def main():
    vk_session = vk_api.VkApi(token=MY_TOKEN)
    long_poll = VkBotLongPoll(vk_session, '210776300')

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.text == "/start":
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button("Button", color=VkKeyboardColor.NEGATIVE)
                send_message(vk_session, event.message.from_id, event.message.text, keyboard)





if __name__ == '__main__':
    main()
