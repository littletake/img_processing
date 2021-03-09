# -*- coding: utf-8 -*-
# クラスを用いて名前変更の部分を分離
# 第一引数: 写真のファイル場所 ex)test"
# 第二引数: GPSデータのCSVファイル

import os
import glob
import sys
from tqdm import tqdm

# import change_name
from code_gps import save

DIR_PATH = os.getcwd()
dirname_img = DIR_PATH + "/" + sys.argv[1]
filename_gps = DIR_PATH + "/" + sys.argv[2]

img_file_list = sorted(glob.glob(dirname_img + "/*"))
print(img_file_list)

for num in tqdm(range(len(img_file_list))):
    # change_name.save_img(img_file_list[num])
    save.save_img(img_file_list[num], filename_gps)
    print(str(num + 1) + "/" + str(len(img_file_list)))
