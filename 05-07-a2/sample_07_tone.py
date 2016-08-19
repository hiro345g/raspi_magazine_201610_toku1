#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, wiringpi

# 定数
SPK_PIN = 5  # 圧電スピーカーのGPIO番号


def main():
    SCALE = [262, 294, 330, 349, 392, 440, 494, 525]  # ドレミファソラシドの周波数値を持つ配列
    wiringpi.wiringPiSetupGpio()  # wiringpi初期化
    wiringpi.softToneCreate(SPK_PIN)  # ソフトウェアトーン初期化
    for v in SCALE:
        wiringpi.softToneWrite(SPK_PIN, v)  # トーン発生
        time.sleep(0.5)  # 同じ音を出力するために処理を遅延
    wiringpi.softToneWrite(SPK_PIN, 0)  # 再生終了


if __name__ == '__main__':
    main()
