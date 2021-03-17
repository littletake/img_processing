# interface層
# データの入力
import glob
import os
import pandas as pd
from abc import ABCMeta, abstractmethod
from tqdm import tqdm
# from typing import Any

from src.usecase.main import Usecase


# interface層の抽象クラス
class Interface_abs(metaclass=ABCMeta):
    @abstractmethod
    def create(
        self,
        path_original_img: str,
        gps_data: object,
    ) -> None:
        pass


# interface層の実体
class Interface(Interface_abs):
    def __init__(
        self,
        usecase: Usecase
    ) -> None:
        self.usecase = usecase

    def create(
        self,
        DIR_PATH: str,
        dict_args: dict,
    ) -> None:
        # ---
        # pathの検証と画像リストの生成
        # ---
        if dict_args["img"] is None:
            raise TypeError("対象画像のディレクトリを指定してください")
        DIR_PATH_IMG = os.path.join(DIR_PATH, dict_args["img"])
        if not os.path.exists(DIR_PATH_IMG):
            raise TypeError("{} は存在しません". format(DIR_PATH_IMG))
        img_file_list = sorted(glob.glob(DIR_PATH_IMG + "/*"))

        # ---
        # gpsデータの有無の確認
        # ---
        if dict_args["gps"] is None:
            # gpsデータ無
            for num in tqdm(range(len(img_file_list))):
                self.usecase.create_new_img(
                    img_file_list[num],
                    None
                )
        else:
            # gpsデータ有
            FILE_PATH_GPS = os.path.join(DIR_PATH, dict_args["gps"])
            if not os.path.exists(FILE_PATH_GPS):
                raise TypeError("{} は存在しません". format(FILE_PATH_GPS))
            gps_data = pd.read_csv(FILE_PATH_GPS).astype(str)

            for num in tqdm(range(len(img_file_list))):
                self.usecase.create_new_img(
                    img_file_list[num],
                    gps_data
                )
