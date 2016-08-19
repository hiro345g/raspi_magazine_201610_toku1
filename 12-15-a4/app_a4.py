#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import app_12_shelve
from pytz import timezone
import datetime
import shutil
import time
import os.path

# - 定数 - #
PNG_ROOT = '/static'
DIR_PNG = '/home/pi/toku1/12-15-a4' + PNG_ROOT
AIR_PRESSURE_PNG = 'air_pressure.png'
HUMIDITY_PNG = 'humidity.png'
TEMPERATURE_PNG = 'temperature.png'
FILE_NAME = '/home/pi/toku1/12-15-a4/bme280_sqlite3.db'
DB_ECHO = False
INTERVAL = 60
MAX_FILE_NUM = 24


def copy_graph(src_file_path):
    """日付がついたファイルをsrc_file_pathからコピー"""
    format = '%Y%m%d%H%M%S'
    current_time_str = datetime.datetime.now().strftime(format)  # 日時文字列の取得
    dest_file_path = src_file_path.replace('.png', '-') + current_time_str + '.png'
    # ファイルをコピー
    shutil.copy(src_file_path, dest_file_path)


def get_graph_file_list(src_file_path):
    """日付がついたファイルのリスト"""
    dir_name = os.path.dirname(src_file_path)
    file_name = os.path.basename(src_file_path).replace('.png', '') + '-'
    files = os.listdir(dir_name)
    # 日付がついたファイルのリストを抽出
    target_file_name_list = [x for x in files if x.startswith(file_name)]
    return target_file_name_list


def delete_graph(src_file_path):
    """日付がついたファイルがMAX_FILE_NUM個を超えるときに古いファイルを削除"""
    # 日付がついたファイルのリストの取得
    target_file_name_list = get_graph_file_list(src_file_path)
    # 日付がついたファイルの数が24個あるか確認
    delete_target_num = len(target_file_name_list) - MAX_FILE_NUM
    if delete_target_num > 0:
        # MAX_FILE_NUM個を超えていたら削除
        file_name_list = list(sorted(target_file_name_list))  # ファイル名のソート済みリスト取得
        delete_target_file_list = file_name_list[0:delete_target_num]  # 先頭から削除対象ファイルを抽出
        for target in delete_target_file_list:
            path = '{0}/{1}'.format(os.path.dirname(src_file_path), target)  # ファイルのパスを作成
            os.remove(path)  # ファイル削除


def gen_json(src_file_path):
    """グラフ画像一覧用JSONの生成"""
    target_file_name_list = get_graph_file_list(src_file_path)  # 日付がついたファイルのリストの取得
    file_name_list = list(reversed(sorted(target_file_name_list)))  # ファイル名の逆順リスト取得
    json_text = '{ "graph_list":['
    for file_name in file_name_list:
        json_text = '{0} "{1}/{2}",'.format(json_text, PNG_ROOT, file_name)
    json_text += ']};'
    if len(file_name_list):
        # file_name_listが1個以上の要素を持っていたら、死後の「,」がついているので削除
        json_text = json_text.replace(',]};', ']}')
    # 書き込むファイルの名前を生成して書き込み
    json_file_name = '{0}{1}'.format('graph_list_', os.path.basename(src_file_path).replace('.png', '.json'))
    json_file_path = '{0}/{1}'.format(DIR_PNG, json_file_name)
    with open(json_file_path, mode='w') as f:
        f.write(json_text)
        f.flush()


def main():
    """ グラフ画像生成メイン処理 """
    # 初期処理
    app_12_shelve.save_app_data(running=True)
    # ファイルの存在チェックと24個分の記録
    running = True
    while running:
        # 各グラフファイルについて繰り返し処理
        for f in [AIR_PRESSURE_PNG, HUMIDITY_PNG, TEMPERATURE_PNG]:
            # ファイルが存在するなら処理を実行
            file_path = '{0}/{1}'.format(DIR_PNG, f)
            if os.path.exists(file_path):
                copy_graph(file_path)  # グラフファイルコピー
                delete_graph(file_path)  # 不要なグラフファイルの削除
                gen_json(file_path)  # JSONデータファイルを生成
        # INTEVAL秒休止
        time.sleep(INTERVAL)
        # 継続チェック
        running = app_12_shelve.load_app_data()


if __name__ == '__main__':
    main()
