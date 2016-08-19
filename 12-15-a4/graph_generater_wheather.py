#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import app_12_shelve
from pytz import timezone
import datetime
import time
import os.path
import seaborn
import pandas
import package_parts.bme280_sqlite3 as db

# - 定数 - #
DIR_PNG = '/home/pi/toku1/12-15-a4/static/'
AIR_PRESSURE_PNG = 'air_pressure.png'
HUMIDITY_PNG = 'humidity.png'
TEMPERATURE_PNG = 'temperature.png'
FILE_NAME = '/home/pi/toku1/12-15-a4/bme280_sqlite3.db'
DB_ECHO = False
INTERVAL = 60


def to_jst(utcnow):
    format = '%Y-%m-%d %H:%M:%S'
    tz_tokyo = timezone('Asia/Tokyo')
    return tz_tokyo.fromutc(utcnow).strftime(format)


def to_jst_hms(utcnow):
    format = '%H:%M:%S'
    tz_tokyo = timezone('Asia/Tokyo')
    return tz_tokyo.fromutc(utcnow).strftime(format)


def generate_png(list, y_label, file_name):
    """ seabornによるグラフ生成 """
    # データがないときは何もしないで終了
    if len(list) == 0:
        return
    elif len(list) > 6:
        end = len(list)
        start = end - 6
        data = list[start:end]
    else:
        data = list
    # 作業用リスト変数の用意
    label_list = []
    created_datetime_list = []
    value_list = []
    # pandas.DataFrame用のデータ用意
    for e in data:
        label_list.append(to_jst_hms(e.created_datetime))  # 時刻だけ取得
        created_datetime_list.append(to_jst(e.created_datetime))  # 秒以下切り捨てにした日時文字列を取得
        value_list.append(int(e.value))  # グラフではint値で表示
    # pandas.DataFrameオブジェクトの作成
    data_frame = pandas.DataFrame(
        {'created_datetime': created_datetime_list,
         y_label: value_list},
        columns=['created_datetime', y_label]
    )
    # seaborn.pointplot()を使ってグラフ生成
    ax = seaborn.pointplot(x='created_datetime', y=y_label, data=data_frame, markers=[''])
    ax.set_xticklabels(label_list)  # x軸の目盛りラベル指定
    seaborn.plt.savefig(DIR_PNG + '/' + file_name)  # 画像保存
    seaborn.plt.clf()


def main():
    """ グラフ画像生成メイン処理 """
    # 初期処理
    app_12_shelve.save_app_data(running=True)
    # seaborn font 指定
    seaborn.set(font='FreeSans')

    # データの取得
    running = True
    while running:
        # DB開始処理
        if os.path.exists(FILE_NAME):
            session = db.start_session(FILE_NAME, DB_ECHO)
        else:
            session = db.start_session_with_createdb(FILE_NAME, DB_ECHO)
        # 対象期間
        current_time = datetime.datetime.now(timezone('UTC'))
        start_time = (current_time - datetime.timedelta(days=1))
        end_time = current_time
        # 気圧
        air_pressure_list = session.query(db.AirPressure).filter(
            db.AirPressure.created_datetime.between(start_time, end_time)).all()
        generate_png(air_pressure_list, 'hPa', AIR_PRESSURE_PNG)
        # 湿度
        humidity_list = session.query(db.Humidity).filter(
            db.Humidity.created_datetime.between(start_time, end_time)).all()
        generate_png(humidity_list, 'Percent', HUMIDITY_PNG)
        # 温度
        temperature_list = session.query(db.Temperature).filter(
            db.Temperature.created_datetime.between(start_time, end_time)).all()
        generate_png(temperature_list, 'C', TEMPERATURE_PNG)
        # DB終了処理
        session.close()
        # INTEVAL秒休止
        time.sleep(INTERVAL)
        # 継続チェック
        running = app_12_shelve.load_app_data()


if __name__ == '__main__':
    main()
