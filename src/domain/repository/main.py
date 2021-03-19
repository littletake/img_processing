# domain層
# domainを扱う処理について定義
from abc import ABCMeta, abstractmethod

from src.domain.model.main import Exif


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def save_img(
        self,
        exif: Exif
    ):
        pass

    def add_gps(
        self,
        exif: Exif
    ):
        pass
