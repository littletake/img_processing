# usecase層
# Exifクラスの作成
# gpsデータがあればExifクラスに追加
from abc import ABCMeta, abstractmethod
# from typing import Any

from src.domain.repository.main import Repository
from src.domain.model.main import Exif
from utils.name import create_new_name


# usecase部分の抽象クラス
class Usecase_abs(metaclass=ABCMeta):
    @abstractmethod
    def create_new_img(
        self,
        path_original_img: str,
        gps_data: object,
    ) -> None:
        pass


# usecase部分の実体
class Usecase(Usecase_abs):
    def __init__(
        self,
        repo: Repository
    ) -> None:
        self.repo = repo

    def create_new_img(
        self,
        path_original_img: str,
        gps_data: object
    ) -> None:

        # 新規画像を作成
        new_img_name = self.__create_name(path_original_img)

        # exifクラスを生成
        new_exif = Exif(
            new_img_name,
            gps_data,
            path_original_img
        )

        # 新規画像の保存
        self.repo.save_img(
            new_exif
        )
        # exifをコピー
        self.repo.add_gps(
            new_exif
        )

    def __create_name(
        self,
        img_name: str
    ) -> str:
        """日付情報を使って適切な名前を生成"""
        new_img_name = create_new_name(img_name)
        return new_img_name
