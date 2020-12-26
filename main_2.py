# -*- coding: utf-8 -*-
# クラスを用いて名前変更の部分を分離
# 第一引数: 写真のファイル場所 ex)test"
# 第二引数: GPSデータのCSVファイル

import os
import glob
import sys
import change_name
# import save

DIR_PATH = os.getcwd()
file_path = DIR_PATH + "/" + sys.argv[1]
# gps_data = DIR_PATH + "/" + sys.argv[2]

# これでファイルのパスのリストが取得できる。
img_file_list = sorted(glob.glob(file_path + "/*"))
print(img_file_list)

for num in range(len(img_file_list)):
    change_name.save_img(img_file_list[num])
    # save.save_img(img_file_list[num], gps_data)
    print(str(num + 1) + "/" + str(len(img_file_list)))
