#
# -*- coding: utf-8 -*-
import shelve

# 変数
app_data = "app_05"


def save_app_05_status(running, led_values, button_values):
    # 指定された running, led_values, button_values を保存
    with shelve.open(app_data) as db:
        db['running'] = running
        db['led_values'] = led_values
        db['button_values'] = button_values


def load_app_05_status():
    with shelve.open(app_data) as db:
        running = db['running']
        led_values = db['led_values']
        button_values = db['button_values']
    return running, led_values, button_values