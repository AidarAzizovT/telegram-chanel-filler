import os

import telebot
from config import TOKEN_TG
bot = telebot.TeleBot(TOKEN_TG)

# Chat ID where you want to send the photos
chat_id = '-1002001719856'

# A list of file paths for the photos
photo_paths = os.listdir('stretched_test/4')
# Send multiple photos in a single message
media = []
for photo in photo_paths:
    if photo.endswith('.txt'):
        continue
    with open(f'stretched_test/4/{photo}', 'rb') as photo_file:
        media.append(telebot.types.InputMediaPhoto(photo_file.read()))

bot.send_media_group(chat_id, media)
