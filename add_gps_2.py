# -*- coding: utf-8 -*-
# パッケージpiexifを使って実装

import piexif
from fractions import Fraction

import export_gps


def add_gpsinfo(img_name, gps_data, exif_dict):
    """
    GPSInfoの部分を新たに作成し既存のexifに付与
    """
    # GPSデータから画像の日時を使って適切な経緯情報を選択
    gps_data = export_gps.export_lat_long_jp(img_name, gps_data)

    if gps_data == [0, 0]:
        # 該当無しの場合
        new_exif_dict = {
            "0th": exif_dict["0th"],
            "Exif": exif_dict["Exif"],
            "Interop": exif_dict["Interop"],
            "1st": exif_dict["1st"],
            "thumbnail": exif_dict["thumbnail"]
        }
        exif_bytes = piexif.dump(new_exif_dict)
        return exif_bytes
    else:
        # 該当有りの場合
        # 経緯の情報を整形
        lat_deg = change_to_deg(gps_data[0], ["S", "N"])
        lng_deg = change_to_deg(gps_data[1], ["W", "E"])
        lat_tuple = (change_to_rational(lat_deg[0]), change_to_rational(
            lat_deg[1]), change_to_rational(lat_deg[2]))
        lng_tuple = (change_to_rational(lng_deg[0]), change_to_rational(
            lng_deg[1]), change_to_rational(lng_deg[2]))
        gps_ifd = {
            piexif.GPSIFD.GPSVersionID: exif_dict['GPS'][0],
            piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
            piexif.GPSIFD.GPSLatitude: lat_tuple,
            piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
            piexif.GPSIFD.GPSLongitude: lng_tuple,
        }
        new_exif_dict = {
            "0th": exif_dict["0th"],
            "Exif": exif_dict["Exif"],
            "GPS": gps_ifd,
            "Interop": exif_dict["Interop"],
            "1st": exif_dict["1st"],
            "thumbnail": exif_dict["thumbnail"]
        }
        exif_bytes = piexif.dump(new_exif_dict)
        return exif_bytes


def change_to_deg(value, loc):
    if value < 0:
        loc_value = loc[0].encode()
    elif value > 0:
        loc_value = loc[1].encode()
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
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
    img_name = "./exif_test/test2.jpg"
    # exif_dic = piexif.load(img_name)
    # gps_info = exif_dic["GPS"]
    # print(gps_info)

    gps_data = "./code_gps/gps_data/2019_9_15-9_19.csv"
    exif_dict = piexif.load(img_name)
    new_exif = add_gpsinfo(img_name, gps_data, exif_dict)
    # gps_data = DIR_PATH + "/" + sys.argv[2]
    # exif_bytes = make_gpsinfo(sys.argv[1], sys.argv[2], exif_dic)
    # piexif.insert(exif_bytes, img_name)
