# -*- coding: utf-8 -*-

'''
GPS情報をcsvファイルから読み込んで写真のexifに付与する
注意点
- 撮影した日にちのgps情報は絶対あること（エラー処理はまだ考えない）
- 時間が一眼は時差考慮済み、GPSは時差考慮していない（標準時間になっている）
- GPSのデータの方を補正する方法をとる

引数
1. 写真のパス
2. csvファイルのパス
'''

# from PIL import Image
# from PIL.ExifTags import TAGS
# import glob
# import piexif

import os
import pandas as pd
import sys
import change_name
import datetime


def export_lat_long(img_name, gps_data_name):
    """
    写真の名前、gps情報のファイルパスを引数として対応する経緯を出力する関数
    """
    DIR_PATH = os.getcwd()
    gps_data_list = []

    # 1.写真読み込みと加工
    img_name = DIR_PATH + "/" + img_name
    # 時刻を整形。csvは2019/8/10, 10:42:22のようになっている
    img_date_origin = change_name.get_date_from_image(img_name)
    img_date_and_time = img_date_origin.split(" ")
    img_date_list = img_date_and_time[0].split(":")
    img_date = img_date_list[0] + "/" + \
        img_date_list[1] + "/" + img_date_list[2]
    img_time = img_date_and_time[1]
    img_time_list = img_time.split(":")
    # print(img_time)

    # gps情報との比較用に作成
    # 日本仕様

    # 2.csvファイル読み込み
    # 時刻的に一番近い位置情報を用いる
    # 0. まず経度を参考に時差を計算して考慮する
    # 1. 時刻が等しい情報がないか検索。あればそれを使う
    # 2. ない場合は時刻差が一番小さいものを使う
    gps_data = pd.read_csv(DIR_PATH + "/" + gps_data_name).astype(str)
    # print(gps_data.loc[:, ' Time'].head())

    # 各データをリスト化
    gps_date_list = gps_data.loc[:, 'Date'].astype(str).tolist()
    gps_time_list = gps_data.loc[:, ' Time'].astype(str).tolist()
    gps_latitude_list = gps_data.loc[:, ' Latitude'].astype(float).tolist()
    gps_longitude_list = gps_data.loc[:, ' Longitude'].astype(float).tolist()

    # 3.GPS情報の経度から時差を計算して時間を補正
    # 公式のパッケージを利用（時間の補正は難しい）
    for num in range(len(gps_longitude_list)):
        gps_date_and_time = gps_date_list[num] + " " + gps_time_list[num]
        print(gps_time_list[num])
        time_diff = int(int(gps_longitude_list[num]) / 15)
        print(time_diff)
        gps_date_and_time = utc_to_jst(gps_date_and_time, time_diff)
        gps_date_list[num] = gps_date_and_time.split(" ")[0]
        gps_time_list[num] = gps_date_and_time.split(" ")[1]
        print(gps_time_list[num])

    #     # 西経
    #     else:
    #         time_diff = (int(gps_longitude_list[num])* -1) / 15 + 9
    #
    #
    #         gps_time_list_list = gps_time_list[num].split(":")
    #         gps_time_hour = int(gps_time_list_list[0]) - time_diff
    #         # 正常に補正完了
    #         if gps_time_hour >= 0:
    #             gps_time_list[num] = str(gps_time_hour) + ":" + gps_time_list_list[1] + ":" + gps_time_list_list[2]
    #         else:
    #             gps_date_list_list = gps_date_list[num].split("/")
    #             if int(gps_date_list_list[2])-1 == 0:
    #                 if int(gps_date_list_list[1])-1 == 0:
    #                     gps_year = int(gps_date_list_list[0])-1
    #                     gps_date_list[num] = str(gps_year) + "/" + gps_date
    #             gps_date_list[num] = gps_date_list_list[0] + gps_date_list_list[1] + str(int(gps_date_list_list[2])-1)
    #
    # # 東経
    # if int(img_time_list[0]) > 0:
    #     time_diff = int(int(img_time_list[0]) / 15)
    #     img_hour = int(img_time_list[0]) - time_diff
    #     if img_hour > 0:
    #         img_time_comp = str(img_hour) + ":" + img_time_list[1] + ":" + img_time_list[2]
    #         print(img_time_comp)
    #     else:
    #         img_date = img_date_list[0] + "/" + img_date_list[1] + "/" + str(int(img_date_list[2])-1)
    #         img_time_comp = str(24 + img_hour) + ":" + img_time_list[1] + ":" + img_time_list[2]
    # # 西経
    # else:
    #     print("No East Longitude")

    start_num = 0
    end_num = 0
    ok_flag = 0  # 適切な位置情報が見つかったかどうかの指針
    # 撮影日の範囲を検索
    for num_date in range(len(gps_date_list)):
        if (gps_date_list[num_date] == img_date) and (start_num == 0):
            start_num = num_date
        if (gps_date_list[num_date] != img_date) and (start_num != 0) and (end_num == 0):
            end_num = num_date
    if end_num == 0:
        end_num = len(gps_date_list)

    # 撮影時刻と比較
    for num in range(start_num, end_num):
        if gps_time_list[num] == img_time_comp:
            img_latitude = gps_latitude_list[num]
            img_longitude = gps_longitude_list[num]
            ok_flag = 1

    # 適切な位置情報が見つからない場合
    if ok_flag == 0:
        date_val_list_img = img_time_comp.split(":")
        date_val_img = int(
            date_val_list_img[0])*3600 + int(date_val_list_img[1])*60 + int(date_val_list_img[2])
        min_diff = 86400  # 1日
        min_num = 0

        for num in range(start_num, end_num):
            date_val_list_gps = gps_time_list[num].split(":")
            date_val_gps = int(
                date_val_list_gps[0])*3600 + int(date_val_list_gps[1])*60 + int(date_val_list_gps[2])
            diff = abs(date_val_gps - date_val_img)
            if min_diff >= diff:
                min_diff = diff
                min_num = num

        img_latitude = gps_latitude_list[min_num]
        img_longitude = gps_longitude_list[min_num]

    gps_data_list.append(img_latitude)
    gps_data_list.append(img_longitude)

    return gps_data_list


def utc_to_jst(timestamp_utc, time_diff):
    datetime_utc = datetime.datetime.strptime(
        timestamp_utc, "%Y/%m/%d %H:%M:%S")
    datetime_jst = datetime_utc.astimezone(
        datetime.timezone(datetime.timedelta(hours=+time_diff)))
    timestamp_jst = datetime.datetime.strftime(
        datetime_jst, '%Y/%m/%d %H:%M:%S')
    return timestamp_jst


if __name__ == '__main__':
    img_name = sys.argv[1]
    gps_data_name = sys.argv[2]
    gps_list = export_lat_long(img_name, gps_data_name)
    print(gps_list[0])
    print(gps_list[1])
