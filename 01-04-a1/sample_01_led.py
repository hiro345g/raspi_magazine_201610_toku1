#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import wiringpi

pin = 4
WAIT_TIME = 5

wiringpi.wiringPiSetupGpio()  # wiringpiの初期化
wiringpi.pinMode(pin, wiringpi.OUTPUT)  # pinを出力モードに
wiringpi.digitalWrite(pin, wiringpi.HIGH)  # LED点灯
time.sleep(WAIT_TIME)  # プログラム休止
wiringpi.digitalWrite(pin, wiringpi.LOW)  # LED消灯
