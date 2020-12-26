# -*- coding: utf-8 -*-
from PIL import Image
import piexif

import change_name
import add_gps_2
import export_gps


# 画像を保存する関数(piexifでexif情報のコピー)
def save_img(img_name, gps_data_name):
    # 改名作業と新規写真の作成
    img = Image.open(img_name)
    new_img_name = change_name.make_name(img_name)
    with Image.new(img.mode, img.size) as dst:
        dst.putdata(img.getdata())
        dst.save(new_img_name, quality=95)
    # piexif.transplant(img_name, new_img_name)

    # 新規写真にジオタグを付与
    exif_dict = piexif.load(img_name)
    exif_bytes = add_gps_2.make_gpsinfo(img_name, gps_data_name, exif_dict)
    piexif.insert(exif_bytes, img_name)

    # gps_list = []
    # gps_list = export_gps.export_lat_long(img_name, gps_data_name)
    #
    # # gps情報を付与(ファイル名, 緯度, 経度)
    # add_gps.set_gps_location(new_img_name, gps_list[0], gps_list[1])
