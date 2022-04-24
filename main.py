import random
import os

import requests
from dotenv import load_dotenv


class VK_Error(TypeError):
    pass


def load_image(url, path, payload=None):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def check_vk_errors(response):
    if "error" in response:
        raise VK_Error(
            "error_code: {0}, error_message: {1}".format(
                response["error"]["error_code"],
                response["error"]["error_msg"],
            )
        )


def load_random_comics(path):
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    all_comics_number = response.json()["num"]
    
    response = requests.get(
        f"https://xkcd.com/{random.randint(0, all_comics_number)}/info.0.json"
    )
    response.raise_for_status()
    response_data = response.json()
    load_image(response_data["img"], path)
    message = response_data["alt"]
    return message


def get_url_to_load(acess_token, group_id):
    payload = {
        "group_id": group_id,
        "v": 5.131,
    }
    headers = {
        "Authorization": f"Bearer {acess_token}"
    }
    response = requests.get(
        "https://api.vk.com/method/photos.getWallUploadServer",
        params=payload,
        headers=headers
    )
    response.raise_for_status()
    response_data = response.json()
    check_vk_errors(response_data)
    upload_url = response_data["response"]["upload_url"]
    return upload_url


def load_to_server(image_path, upload_url):
    with open(image_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        response_data = response.json()
        check_vk_errors(response_data)
        comics_server = response_data["server"]
        comics_hash = response_data["hash"]
        comics_photo = response_data["photo"]
    return comics_server, comics_hash, comics_photo


def upload_to_wall(comics_server, comics_hash, comics_photo, acess_token, group_id):
    headers = {
        "Authorization": f"Bearer {acess_token}"
    }
    payload = {
        "group_id": group_id,
        "v": 5.131,
        "server": comics_server,
        "hash": comics_hash,
        "photo": comics_photo
    }
    response = requests.get(
        "https://api.vk.com/method/photos.saveWallPhoto",
        params=payload,
        headers=headers
    )
    response.raise_for_status()
    response_data = response.json()
    check_vk_errors(response_data)
    owner_id = response_data["response"][0]["owner_id"]
    media_id = response_data["response"][0]["id"]

    return owner_id, media_id


def publish(owner_id, media_id, message, acess_token, group_id):
    headers = {
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
        headers=headers
    )
    response.raise_for_status()
    check_vk_errors(response.json())


def main():
    load_dotenv()

    try:
        comics_path = "comics.jpg"

        group_id = int(os.environ['GROUP_ID'])
        acess_token = os.environ['ACESS_TOKEN']

        message = load_random_comics(comics_path)


        upload_url = get_url_to_load(acess_token, group_id)

        comics_server, comics_hash, comics_photo = load_to_server(comics_path, upload_url)

        owner_id, media_id = upload_to_wall(
            comics_server,
            comics_hash,
            comics_photo,
            acess_token,
            group_id
        )

        publish(owner_id, media_id, message, acess_token, group_id)
    finally:
        os.remove("comics.jpg")


if __name__ == "__main__":
    main()
