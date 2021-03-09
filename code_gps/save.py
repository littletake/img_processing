# -*- coding: utf-8 -*-
from PIL import Image
import piexif

from name import create_new_name
import add_gps_2


def save_img(img_name, gps_data_name):
    """
    画像を保存する関数
    """
    # 改名作業と新規写真の作成
    img = Image.open(img_name)
    new_img_name = create_new_name(img_name)
    with Image.new(img.mode, img.size) as dst:
        dst.putdata(img.getdata())
        dst.save(new_img_name, quality=95)

    # 新規写真にジオタグを付与
    exif_dict = piexif.load(img_name)
    exif_bytes = add_gps_2.add_gpsinfo(img_name, gps_data_name, exif_dict)
    piexif.insert(exif_bytes, new_img_name)
