#
# -*- coding: utf-8 -*-
import shelve

# 変数
app_data = "app_03"


def save_led_pwm_list(running, led_values):
    # 指定された running, led_values を保存
    with shelve.open(app_data) as db:
        db['running'] = running
        db['led_values'] = led_values


def load_led_pwm_list():
    with shelve.open(app_data) as db:
        running = db['running']
        led_values = db['led_values']
    return running, led_values