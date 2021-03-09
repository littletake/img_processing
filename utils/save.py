# -*- coding: utf-8 -*-
# TODO: 依存方向が間違っている気がする
from PIL import Image
import piexif

from utils.name import create_new_name
from utils.add_gps import add_gpsinfo


def create_name_and_save(img_name):
    # 改名作業と新規写真の作成
    img = Image.open(img_name)
    new_img_name = create_new_name(img_name)
    with Image.new(img.mode, img.size) as dst:
        dst.putdata(img.getdata())
        dst.save(new_img_name, quality=95)
    return new_img_name


def save_img(img_name, gps_data):
    """
    名称を日時に変更しジオタグを付与した画像の保存
    """
    new_img_name = create_name_and_save(img_name)
    # # 改名作業と新規写真の作成
    # img = Image.open(img_name)
    # new_img_name = create_new_name(img_name)
    # with Image.new(img.mode, img.size) as dst:
    #     dst.putdata(img.getdata())
    #     dst.save(new_img_name, quality=95)

    # 新規写真にジオタグを付与
    exif_dict = piexif.load(img_name)
    exif_bytes = add_gpsinfo(img_name, gps_data, exif_dict)
    piexif.insert(exif_bytes, new_img_name)


def save_img_only(img_name):
    """
    名称を日時に変更した画像の保存
    """
    new_img_name = create_name_and_save(img_name)
    # img = Image.open(img_name)
    # new_img_name = create_new_name(img_name)
    # with Image.new(img.mode, img.size) as dst:
    #     dst.putdata(img.getdata())
    #     dst.save(new_img_name, quality=95)

    # exifをコピー
    piexif.transplant(img_name, new_img_name)
