#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts.parts import Led as Led
from package_parts.parts import Button as Button
import sys, time
import app_05_db

# -- 定数宣言 -- #
LED_PINS = [4]  # LEDのGPIO番号
BUTTON_PINS = [13]  # ボタンのGPIO番号
GPIO_HIGH = 1
GPIO_LOW = 0


# -- 関数 -- #
def get_status_list(led_list, button_list):
    """LEDとスイッチの状態をled_values, button_valuesのリストにする"""
    led_values = []
    for e in led_list:
        led_values.append(e.get_status())
    button_values = []
    for e in button_list:
        button_values.append(e.get_status())
    return led_values, button_values


def load(led_list, button_list):
    """ 保存データ取得
      スイッチは状態の指定はプログラムからはできないので反映しない
    """
    running, led_values, button_values = app_05_db.load_app_05_status()
    for i in range(len(led_values)):
        led_list[i].set_status(led_values[i])
    return running, led_list, button_list


def save(running, led_list, button_list):
    """ データ保存 """
    led_values, button_values = get_status_list(led_list, button_list)
    app_05_db.save_app_05_status(running, led_values, button_values)


def init():
    """ LEDとスイッチの初期化 """
    led_list = []
    for led in LED_PINS:
        led_list.append(Led(led))
    button_list = []
    for button in BUTTON_PINS:
        button_list.append(Button(button))
    return led_list, button_list


def main(interval):
    """メイン処理
      スイッチを押すとLEDが点灯、離すと消灯
      状態をapp_05.dbファイルへ保存
      app_05.dbのrunningがFalseになると停止
    """
    led_list, button_list = init()
    running = True
    save(running, led_list, button_list)  # 現在の状態を保存

    v0 = GPIO_LOW
    print('app_05 start')
    while running:  # runningがTrueの間、処理をし続ける
        # スイッチの値をチェック
        v = button_list[0].get_status()
        if v0 != v:
            # 値が変更されていたら状態保存
            led_list[0].set_status(v)
            save(running, led_list, button_list)
            v0 = v
        # interval秒間、現在の設定のまま維持
        time.sleep(interval)
        # interval秒毎にアプリのデータをチェック
        running, led_list, button_list = load(led_list, button_list)
    print('app_05 stop')


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    argv_interval = 0.1
    if len(sys.argv) > 1:
        argv_interval = int(sys.argv[1])
    main(argv_interval)
