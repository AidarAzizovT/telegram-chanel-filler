import os
import telebot
from config import TOKEN_TG


bot = telebot.TeleBot(TOKEN_TG)


def post_to_tg(group_name, post_id):
    try:
        if len(os.listdir(f'{group_name}/{post_id}')) == 2:
            with open(f'{group_name}/{post_id}/text.txt', 'r', encoding='utf-8') as file:
                text_of_mes = file.read()
            with open(f'{group_name}/{post_id}/{post_id}.jpg', 'rb') as photo:
                bot.send_photo('-1002001719856', photo, caption=text_of_mes)
        else:
            with open(f'{group_name}/{post_id}/text.txt', 'r', encoding='utf-8') as file:
                text_of_mes = file.read()
            media = []
            for file in os.listdir(f'{group_name}/{post_id}'):
                if file.endswith('.txt'):
                    continue
                with open(f'{group_name}/{post_id}/{file}', 'rb') as photo_file:
                    media.append(telebot.types.InputMediaPhoto(photo_file.read()))

            bot.send_media_group('-1002001719856', media)
            bot.send_message('-1002001719856', text_of_mes)
    except Exception:
        print(Exception)
