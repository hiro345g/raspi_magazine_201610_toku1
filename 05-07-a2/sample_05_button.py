#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import wiringpi

# 定数宣言
LED_PIN = 4  # LEDのGPIO番号
BUTTON_PIN = 13  # スイッチのGPIO番号
BUTTON_DELAY = 0.5  # チャタリング防止用の遅延時間
INTERVAL = 0.1  # スイッチチェック間隔


def get_button_value(pin):
    """指定したpinのスイッチ入力状態を取得"""
    v = wiringpi.digitalRead(pin)
    if v == wiringpi.HIGH:
        # チャタリング防止のため次回の入力チェックを遅らせる
        time.sleep(BUTTON_DELAY)
    return v


def main():
    """メイン処理"""
    wiringpi.wiringPiSetupGpio()  # wiringpiの初期化
    wiringpi.pinMode(LED_PIN, wiringpi.OUTPUT)  # LEDは出力モード
    wiringpi.pinMode(BUTTON_PIN, wiringpi.INPUT)  # スイッチは入力モード
    cnt = 0
    current_led_value = wiringpi.LOW
    try:
        while cnt < 4:
            # cnt が4になるまで繰り返し
            button_value = get_button_value(BUTTON_PIN)
            if button_value == wiringpi.HIGH:
                cnt += 1
                print('cnt:{0}'.format(cnt))
                if current_led_value == wiringpi.HIGH:
                    wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)
                    current_led_value = wiringpi.LOW
                else:
                    wiringpi.digitalWrite(LED_PIN, wiringpi.HIGH)
                    current_led_value = wiringpi.HIGH
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)


if __name__ == '__main__':
    main()
