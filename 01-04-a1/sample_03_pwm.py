#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, wiringpi

# 定数宣言
LED_PINS = [17, 27, 22]  # LEDのGPIO番号
LED_PWM_RANGE = 100
INTERVAL = 0.1

# 初期化
wiringpi.wiringPiSetupGpio()
for led in LED_PINS:
    wiringpi.pinMode(led, wiringpi.OUTPUT)
    wiringpi.softPwmCreate(led, 0, LED_PWM_RANGE)

# 現在の設定値を反映
for v in range(LED_PWM_RANGE):
    for led in LED_PINS:
        wiringpi.softPwmWrite(led, v)
    time.sleep(INTERVAL)

# LEDをすべて消灯
for led in LED_PINS:
    wiringpi.softPwmWrite(led, 0)
