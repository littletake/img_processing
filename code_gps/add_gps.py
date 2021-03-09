# -*- coding: utf-8 -*-

# pyexiv2パッケージを使用
# gps情報を写真のexifに付与する
# 参考サイト : https://www.gis-py.com/entry/2016/01/20/173253

import pyexiv2
from PIL import Image


def to_deg(value, loc):
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return (deg, min, sec, loc_value)


def set_gps_location(file_name, lat, lng):

    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    # 緯度、経度を10進法→60進法(度分秒)に変換
    exiv_lat = (pyexiv2.Rational(lat_deg[0] * 60 + lat_deg[1], 60),
                pyexiv2.Rational(lat_deg[2] * 100, 6000), pyexiv2.Rational(0, 1))
    exiv_lng = (pyexiv2.Rational(lng_deg[0] * 60 + lng_deg[1], 60),
                pyexiv2.Rational(lng_deg[2] * 100, 6000), pyexiv2.Rational(0, 1))
    metadata = pyexiv2.ImageMetadata(file_name)
    metadata.read()

    # メタデータを付与
    metadata["Exif.GPSInfo.GPSLatitude"] = exiv_lat
    metadata["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
    metadata["Exif.GPSInfo.GPSLongitude"] = exiv_lng
    metadata["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
    metadata["Exif.Image.GPSTag"] = 654
    metadata["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
    metadata["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'

    # メタデータを上書き
    metadata.write()
