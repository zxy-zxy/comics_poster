import json

import requests


class VkPosterException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VkPoster:
    def __init__(self, access_token, group_id, image_path, message):
        self.params = {
            'v': 5.92,
            'access_token': access_token
        }
        self._vk_url = 'https://api.vk.com/method'
        self._group_id = group_id
        self._image_path = image_path
        self._message = message
        self._img_upload_url = None
        self._server = None
        self._photo = None
        self._hash = None
        self._owner_id = None
        self._media_id = None

    def _make_request(self, method, url, params, files=None):
        method = getattr(requests, method)
        try:
            response = method(url, params=params, files=files)
        except requests.RequestException as e:
            raise VkPosterException(f'An error has occurred during call to {url}: {e}')

        try:
            json_response = response.json()
        except json.JSONDecodeError as e:
            raise VkPosterException(f'An error has occurred during parsing response from {url}: {e}')

        if not response.ok:
            raise VkPosterException(f'Response from {url} is not ok: {json_response}')

        if 'error' in json_response.keys():
            error_msg = json_response['error']['error_msg']
            raise VkPosterException(f'Response from {url} contains errors: {error_msg}')

        return json_response

    def get_image_url_upload(self):
        url = f'{self._vk_url}/photos.getWallUploadServer'
        params = dict()
        params.update(self.params)
        response = self._make_request('get', url, params)
        self._img_upload_url = response['response']['upload_url']
        return self

    def upload_image(self):
        params = dict()
        params.update(self.params)
        image_file_opened = open(self._image_path, 'rb')
        files = {'photo': image_file_opened}
        response = self._make_request('post', self._img_upload_url, params, files)
        self._server = response['server']
        self._photo = response['photo']
        self._hash = response['hash']
        return self

    def save_image(self):
        url = f'{self._vk_url}/photos.saveWallPhoto'
        params = dict()
        params.update(self.params)
        params['server'] = self._server
        params['photo'] = self._photo
        params['hash'] = self._hash
        response = self._make_request('post', url, params)
        self._owner_id = response['response'][0]['owner_id']
        self._media_id = response['response'][0]['id']
        return self

    def post_image_on_wall(self):
        url = f'{self._vk_url}/wall.post'
        attachment = f'photo{self._owner_id}_{self._media_id}'
        params = dict()
        params.update(self.params)
        params['message'] = self._message
        params['owner_id'] = f'-{self._group_id}'
        params['attachments'] = [attachment]
        response = self._make_request('post', url, params)
        return self
