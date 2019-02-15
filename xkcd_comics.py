import os
import requests


class XKCDComicsException(Exception):
    pass


class XKCDComics:
    def __init__(self, num, title, img_url):
        self.num = num
        self.title = title
        self.img_url = img_url
        self._img_path = None

    def __repr__(self):
        return f'Number: {self.num}, Title: {self.title}, img: {self.img_url}'

    @property
    def img_path(self):
        if self._img_path is None or not os.path.isfile(self._img_path):
            self._load_comics_image_from_url()
        return self._img_path

    def delete_img(self):
        if self._img_path:
            os.remove(self._img_path)
        self._img_path = None

    def _load_comics_image_from_url(self):
        img_bytes = self._load_img()
        self._img_path = self._save_img(img_bytes)

    def _load_img(self):
        try:
            img_response = requests.get(self.img_url)
        except requests.RequestException as e:
            raise XKCDComicsException(
                f'Cannot load image {self.img_url} from internet: {e}'
            )
        return img_response.content

    def _extract_filename_from_url(self):
        url_without_extension, extension = os.path.splitext(self.img_url)
        filename = url_without_extension.split('/')[-1]
        return f'{filename}{extension}'

    def _save_img(self, image_bytes):
        filename = self._extract_filename_from_url()
        try:
            with open(filename, "wb") as file:
                file.write(image_bytes)
            return filename
        except IOError as e:
            raise XKCDComicsException(
                f'Cannot save image file from {self._img_url}: {e}'
            )
