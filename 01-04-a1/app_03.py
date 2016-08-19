#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, wiringpi
import app_03_db

# 定数宣言
LED_PINS = [17, 27, 22]  # LEDのGPIO番号
LED_PWM_RANGE = 100


# 関数
def led_list_off():
    """LEDをすべて消灯"""
    for led in LED_PINS:
        wiringpi.softPwmWrite(led, 0)


def init():
    """GPIOとLEDの初期化"""
    wiringpi.wiringPiSetupGpio()
    for index, led in enumerate(LED_PINS):
        wiringpi.pinMode(led, wiringpi.OUTPUT)
        wiringpi.softPwmCreate(led, 0, LED_PWM_RANGE)


def main(led_values, interval):
    """LEDをソフトウェアPWMで点灯するメイン処理"""
    init()
    led_list_off()
    running = True
    # 指定された led_values を保存
    app_03_db.save_led_pwm_list(running, led_values)

    # runningがTrueの間、処理をし続ける
    led_last_values = led_values[:]  # led_valuesの値を現在値として保存
    while running:
        # 現在の値とled_valuesの値と比較して違っていたら現在の設定値を更新
        for index in range(len(LED_PINS)):
            if led_last_values[index] != led_values[index]:
                led_last_values[index] = led_values[index]
                wiringpi.softPwmWrite(LED_PINS[index], led_values[index])
        # interval秒間、現在の設定のまま維持
        time.sleep(interval)
        # interval秒毎にアプリのデータをチェック
        running, led_values = app_03_db.load_led_pwm_list()


if __name__ == '__main__':
    """コンソールアプリとして起動するときの処理"""
    values = [0, 0, 0]
    interval = 1
    if len(sys.argv) > 3:
        for i, v in enumerate(sys.argv[1:4]):
            values[i] = int(v)
            print(v)
    if len(sys.argv) == 5:
        interval = int(sys.argv[4])
    try:
        main(values, interval)
    finally:
        led_list_off()
