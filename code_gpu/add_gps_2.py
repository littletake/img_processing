# -*- coding: utf-8 -*-

# パッケージpiexifを使ってみる
# このコードだとexifを新規で作成するものになってしまう、だから既存のexifに位置情報を追加することを考える。

from PIL import Image
import piexif
import sys
import os
from fractions import Fraction

import change_name
import export_gps

# 画像のパスから画像のexif情報を辞書型で取得
# GPSの部分だけを変更させる

# GPSInfoの部分を作成する関数
def make_gpsinfo(img_name, gps_data_name, exif_dict):
    gps_data = []
    gps_data = export_gps.export_lat_long(img_name, gps_data_name)
    # 経緯の情報を整形
    lat_deg = change_to_deg(gps_data[0], ["S", "N"])
    lng_deg = change_to_deg(gps_data[1], ["W", "E"])
    # print(lat_deg)
    # print(lng_deg)
    # 経緯の情報をジオタグに合わせる
    lat_tuple = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    lng_tuple = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: exif_dict['GPS'][0],
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: lat_tuple,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: lng_tuple,
    }
    exif_dict['GPS'] = {"GPS": gps_ifd}
    print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

def change_to_deg(value, loc):
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)

def change_to_rational(value):
    # 分数値に変換
    '''
    引数: 数
    返り値: tuple ex) (1, 2), (numerator, denominator)
    '''
    f = Fraction(str(value))
    return (f.numerator, f.denominator)


if __name__ == '__main__':
    DIR_PATH = os.getcwd()
    img_name = DIR_PATH + "/" + sys.argv[1]
    exif_dic = piexif.load(img_name)
    gps_info = exif_dic["GPS"]
    print(gps_info)

    gps_data = DIR_PATH + "/" + sys.argv[2]
    exif_bytes = make_gpsinfo(sys.argv[1], sys.argv[2], exif_dic)
    piexif.insert(exif_bytes, img_name)
