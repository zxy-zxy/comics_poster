import os
import requests


class XKCDComicsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class XKCDComics:
    attribute_map = {
        'num': '_num',
        'title': '_title',
        'img': '_img_url'
    }

    def __init__(self, *args, **kwargs):
        for attribute_key in XKCDComics.attribute_map.keys():
            try:
                attribute_value = kwargs[attribute_key]
            except KeyError:
                raise TypeError(
                    f'Attribute {attribute_key} is required to initialization.')
            class_attribute_key = XKCDComics.attribute_map[attribute_key]
            setattr(self, class_attribute_key, attribute_value)
        self._img_path = None

    def __repr__(self):
        return ", ".join(
            [
                "{}:{}".format(attr, getattr(self, attr))
                for attr in self.__dict__
                if not attr.startswith("__")
            ]
        )

    @property
    def num(self):
        return self._num

    @property
    def title(self):
        return self._title

    @property
    def img_path(self):
        if self._img_path is None or not os.path.isfile(self._img_path):
            self._load_comics_image_from_url()
        return self._img_path

    def delete_img(self):
        if self._img_path:
            if self._img_path:
                os.remove(self._img_path)
            self._img_path = None

    def _load_comics_image_from_url(self):
        img_bytes = self._load_img()
        self._img_path = self._save_img(img_bytes)

    def _load_img(self):
        try:
            img_response = requests.get(self._img_url)
        except requests.RequestException as e:
            raise XKCDComicsException(
                f'Cannot load image {self._img_url} from internet: {e}'
            )
        return img_response.content

    def _extract_filename_from_url(self):
        url_without_extension, extension = os.path.splitext(self._img_url)
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
