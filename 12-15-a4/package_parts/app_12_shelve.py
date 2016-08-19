# -*- coding: utf-8 -*-
#
import shelve

# 変数
app_data = "app_12_datalogger_setting"


def save_app_data(running):
    # 指定された running を保存
    with shelve.open(app_data) as db:
        db['running'] = running


def load_app_data():
    with shelve.open(app_data) as db:
        running = db['running']
    return running