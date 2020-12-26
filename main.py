# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
import os
import glob
import piexif

DIR_PATH = os.getcwd()


# 指定した画像のEXIFデータを取り出す関数
def get_exif_of_image(file):
    image = Image.open(file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        exif_info = image._getexif()
    except AttributeError:
        return {}
    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    exif_table = {}
    for tag_id, value in exif_info.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    return exif_table


# 指定した画像の Exif データのうち日付データを取り出す関数
def get_date_from_image(file):
    """Get date date of an image if exists

    指定した画像の Exif データのうち日付データを取り出す関数
    @return yyyy:mm:dd HH:MM:SS 形式の文字列
    """

    # get_exif_of_imageの戻り値のうち
    # 日付データのみを取得して返す
    exif_table = get_exif_of_image(file)
    return exif_table.get("DateTimeOriginal")


# 適切な形に名前を作成する関数(保存するフォルダも作成)
def make_name(img_name):
    img_date_origin = get_date_from_image(img_name)

    # 文字列のリスト作成
    # 日付と時間を分ける
    img_date_list = img_date_origin.split(" ")
    img_date_not_time = img_date_list[0].split(":")
    img_time = img_date_list[1].split(":")

    # ：を＿に変える
    img_date = img_date_not_time[0] + "_" + img_date_not_time[1] + "_" + img_date_not_time[2]
    img_time = img_time[0] + "_" + img_time[1] + "_" + img_time[2]
    img_full_name = img_date + "_" + img_time

    # 日時のフォルダを作成
    new_dir_path = DIR_PATH + "/" + str(img_date)
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    dir_path = new_dir_path + "/" + img_full_name + ".jpg"
    return dir_path


# 画像を保存する関数(piexifでexif情報のコピー)
def save_img(img_name):
    img = Image.open(img_name)
    new_img_name = make_name(img_name)
    with Image.new(img.mode, img.size) as dst:
        dst.putdata(img.getdata())
        dst.save(new_img_name, quality=95)
    piexif.transplant(img_name, new_img_name)


if __name__ == "__main__":
    file_path = DIR_PATH + "/" + "test"

    # これでファイルのパスのリストが取得できる。
    img_file_list = sorted(glob.glob(file_path + "/*"))
    print(img_file_list)

    for num in range(len(img_file_list)):
        save_img(img_file_list[num])
        print(str(num + 1) + "/" + str(len(img_file_list)))
