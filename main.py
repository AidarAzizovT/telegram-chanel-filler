import json
from tg_fill import post_to_tg
from config import TOKEN_VK
import requests
import os
from time import sleep

groups = ['fitnessed']

def fill_last_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&access_token={TOKEN_VK}&v=5.131&count=2"
    response = requests.get(url).json()['response']['items']
    if os.path.exists(group_name):
        print('Directory already exists')
    else:
        os.mkdir(group_name)
    fresh_post_ids = []
    for post in response:
        fresh_post_ids.append(post['id'])

    if not os.path.exists(f'{group_name}/exists_posts_{group_name}.json'):
        print('File with IDs of files does not exists, I create it')
    with open(f'{group_name}/exists_posts_{group_name}.json', 'w', encoding='utf-8') as file:
        json.dump(fresh_post_ids, file, indent=3, ensure_ascii=False)


def get_max_photo_url(sizes):
    max_height = 0
    url_of_max = ''
    for size in sizes:
        if size['height'] > max_height:
            max_height = size['height']
            url_of_max = size['url']
    return url_of_max


def check_for_new_posts(group_name='fitnessed'):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&access_token={TOKEN_VK}&v=5.131&count=2"
    response = requests.get(url).json()['response']['items']

    if not os.path.exists(group_name):
        print('Directory does not  exists. I create it.')
        os.mkdir(f'{group_name}')
    if not os.path.exists(f'{group_name}/exists_posts_{group_name}.json'):
        with open(f'{group_name}/exists_posts_{group_name}.json', 'w') as file:
            json.dump([], file)

    with open(f'{group_name}/exists_posts_{group_name}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    if len(response) < 2:
        return -1
    if response[1]['id'] not in data:
        data.append(response[1]['id'])
        with open(f'{group_name}/exists_posts_{group_name}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=3)
        return response[1]['id']
    else:
        return -1

def get_data(post_id, group_name='fitnessed'):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&access_token={TOKEN_VK}&v=5.131&count=2"
    response = requests.get(url).json()['response']['items']
    if os.path.exists(group_name):
        print('Directory already exists')
    else:
        os.mkdir(group_name)
    for post in response:
        if post['id'] == post_id:
            if not os.path.exists(f'{group_name}/{post_id}'):
                os.mkdir(f'{group_name}/{post_id}')
            with open(f'{group_name}/{post_id}/text.txt', 'w', encoding='utf-8') as file:
                file.write(post['text'])
            try:
                if 'attachments' in post:
                    attachments = post['attachments']
                    if len(attachments) == 1:
                        if attachments[0]['type'] == 'photo':
                            attach = attachments[0]['photo']
                            url_of_img = get_max_photo_url(attach['sizes'])
                            res = requests.get(url_of_img)
                            if not os.path.exists(f'{group_name}/{post_id}'):
                                os.mkdir(f'{group_name}/{post_id}')
                            with open(f'{group_name}/{post_id}/{post_id}.jpg', 'wb') as img:
                                img.write(res.content)
                    else:
                        index_of_photo = 0
                        for attach in attachments:
                            if attach['type'] == 'photo':
                                attach = attach['photo']
                                url_of_img = get_max_photo_url(attach['sizes'])
                                res = requests.get(url_of_img)
                                if not os.path.exists(f'{group_name}/{post_id}'):
                                    os.mkdir(f'{group_name}/{post_id}')
                                with open(f'{group_name}/{post_id}/{post_id}_{index_of_photo}.jpg', 'wb') as img:
                                    img.write(res.content)
                                index_of_photo += 1

            except Exception:
                print(f'Error with post {post_id}')


group_name = 'xuexinuli'
#fill_last_posts(group_name)

while True:
    id_of_post = check_for_new_posts(group_name=group_name)
    if id_of_post != -1:
        get_data(id_of_post, group_name=group_name)
        post_to_tg(group_name, id_of_post)
        sleep_time = 1
    else:
        sleep_time = 1
    sleep(sleep_time)

