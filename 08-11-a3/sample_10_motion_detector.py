#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import parts
import time

SB412A_PIN = 21  # 人感センサーのGPIO

# SB412A人感センサーを使用
sb412a = parts.Sb412a(SB412A_PIN)
try:
    while True:
        # 人感センサーから値を取得し続ける
        if sb412a.is_on():
            print ("Motion Detector: ON")
        else:
            print ("Motion Detector: OFF")
        time.sleep(1)
except KeyboardInterrupt:
    # キーボードから Ctrl+C が入力されたら終了
    print('KeyboardInterrupt')
