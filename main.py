# -*- coding: utf-8 -*-

import argparse
import glob
import os
import pandas as pd
from tqdm import tqdm

from utils.save import save_img_only, save_img

"""args"""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--img",
    type=str,
    help="画像ディレクトリの名称"
)
parser.add_argument(
    "--gps",
    type=str,
    help="GPSファイルの名称"
)
args = parser.parse_args()
dict_args = vars(args)


"""path"""
DIR_PATH = os.path.dirname(__file__)
if dict_args["img"] is None:
    raise TypeError("対象画像のディレクトリを指定してください")

DIR_PATH_IMG = os.path.join(DIR_PATH, dict_args["img"])
if not os.path.exists(DIR_PATH_IMG):
    raise TypeError("{} は存在しません". format(DIR_PATH_IMG))

img_file_list = sorted(glob.glob(DIR_PATH_IMG + "/*"))


"""code"""
if dict_args["gps"] is None:
    # gpsデータ無し
    for num in tqdm(range(len(img_file_list))):
        save_img_only(img_file_list[num])
else:
    # gpsデータ有り
    FILE_PATH_GPS = os.path.join(DIR_PATH, dict_args["gps"])
    if not os.path.exists(FILE_PATH_GPS):
        raise TypeError("{} は存在しません". format(FILE_PATH_GPS))
    gps_data = pd.read_csv(FILE_PATH_GPS).astype(str)

    for num in tqdm(range(len(img_file_list))):
        save_img(img_file_list[num], gps_data)
