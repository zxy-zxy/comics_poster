import sys
import os
import json
import random

import requests
from dotenv import load_dotenv

from xkcd_comics import XKCDComics, XKCDComicsException
from vk_poster import VkPoster

if __name__ == '__main__':

    comics_url = "https://xkcd.com/{}/info.0.json"

    load_dotenv()

    vk_auth_token = os.getenv('vk_auth_token')
    vk_group_id = os.getenv('vk_group_id')

    last_comics_response = requests.get(comics_url.format(''))
    try:
        last_comics_response_json = last_comics_response.json()
    except json.JSONDecodeError as e:
        sys.exit(f'An error has occurred during parsing response {e}.')

    try:
        last_xkcd_comics = XKCDComics(
            last_comics_response_json['num'],
            last_comics_response_json['title'],
            last_comics_response_json['img'],
        )
    except XKCDComicsException as e:
        sys.exit(f'An error has occurred object initialization {e}.')

    random_comics_number = random.randint(0, last_xkcd_comics.num)

    comics_response = requests.get(comics_url.format(f'{random_comics_number}'))
    try:
        comics_response_json = comics_response.json()
    except json.JSONDecodeError as e:
        sys.exit(f'An error has occurred during parsing response {e}.')

    try:
        xkcd_comics = XKCDComics(
            comics_response_json['num'],
            comics_response_json['title'],
            comics_response_json['img'],
        )
    except XKCDComicsException as e:
        sys.exit(f'An error has occurred object initialization {e}.')

    vk_poster = VkPoster(
        access_token=vk_auth_token,
        group_id=vk_group_id,
        image_path=xkcd_comics.img_path,
        message=xkcd_comics.title,
    )
    vk_poster.init_upload_image_to_server().upload_image().save_image().post_image_on_wall()

    xkcd_comics.delete_img()

    print(f'Comics {random_comics_number} has been successfully posted.')
