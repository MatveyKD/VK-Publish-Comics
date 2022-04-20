import random
import os

import requests
from dotenv import load_dotenv


def load_image(url, path, payload=None):    
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)

def load_comics(path):
    response = requests.get(f"https://xkcd.com/{random.randint(0, 2609)}/info.0.json")
    response.raise_for_status()
    load_image(response.json()["img"], path)
    message = response.json()["alt"]
    return message

def get_url_to_load(acess_token, group_id):
    payload = {
        "group_id": group_id,
        "v": 5.131,
    }
    head = {
        "Authorization": f"Bearer {acess_token}"
    }
    response = requests.get(
        "https://api.vk.com/method/photos.getWallUploadServer",
        params=payload,
        headers=head
    )
    response.raise_for_status()
    upload_url = response.json()["response"]["upload_url"]
    return upload_url

def load_to_server(image_path, upload_url):
    with open(image_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server = response.json()["server"]
        hash = response.json()["hash"]
        photo = response.json()["photo"]
    return server, hash, photo

def upload_to_wall(server, hash, photo, acess_token, group_id):
    head = {
        "Authorization": f"Bearer {acess_token}"
    }
    payload = {
        "group_id": group_id,
        "v": 5.131,
        "server": server,
        "hash": hash,
        "photo": photo
    }
    response = requests.get(
        "https://api.vk.com/method/photos.saveWallPhoto",
        params=payload,
        headers=head
    )
    response.raise_for_status()
    owner_id = response.json()["response"][0]["owner_id"]
    media_id = response.json()["response"][0]["id"]

    return owner_id, media_id

def publish(owner_id, media_id, message, acess_token, group_id):
    head = {
        "Authorization": f"Bearer {acess_token}"
    }
    payload = {
        "owner_id": -group_id,
        "v": 5.131,
        "attachments": f"photo{owner_id}_{media_id}",
        "message": message
    }
    
    response = requests.post(
        "https://api.vk.com/method/wall.post",
        params=payload,
        headers=head
    )
    response.raise_for_status()


if __name__ == "__main__":
    load_dotenv()

    comics_path = "comics.jpg"

    group_id = int(os.environ['GROUP_ID'])
    acess_token = os.environ['ACESS_TOKEN']

    #Скачивание комикса
    message = load_comics(comics_path)

    #Получение адреса для загрузки фото
    upload_url = get_url_to_load(acess_token, group_id)
    
    #Загрузка на сервер
    server, hash, photo = load_to_server(comics_path, upload_url)
    
    #Загрузка на стену
    owner_id, media_id = upload_to_wall(server, hash, photo, acess_token, group_id)
    
    #Публикация
    publish(owner_id, media_id, message, acess_token, group_id)

    
    #Удаление комикса
    os.remove(comics_path)

