import random
import os

import requests
from dotenv import load_dotenv


def load_image(url, path, payload=None):    
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    load_dotenv()

    #Скачивание комикса
    response = requests.get(f"https://xkcd.com/{random.randint(0, 2609)}/info.0.json")
    response.raise_for_status()
    load_image(response.json()["img"], "comics.jpg")
    message = response.json()["alt"]
    
    
    #Получение адреса для загрузки фото
    payload = {
        "group_id": int(os.environ['GROUP_ID']),
        "v": 5.131,
    }
    head = {
        "Authorization": f"Bearer {os.environ['ACESS_TOKEN']}"
    }
    response = requests.get(
        "https://api.vk.com/method/photos.getWallUploadServer",
        params=payload,
        headers=head
    )
    response.raise_for_status()
    upload_url = response.json()["response"]["upload_url"]
    
    #Загрузка на сервер
    with open('comics.jpg', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server = response.json()["server"]
        hash = response.json()["hash"]
        photo = response.json()["photo"]
    
    #Загрузка на стену
    payload = {
        "group_id": int(os.environ['GROUP_ID']),
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
    
    #Публикация
    payload = {
        "owner_id": -int(os.environ['GROUP_ID']),
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

    
    #Удаление комикса
    os.remove("comics.jpg")
