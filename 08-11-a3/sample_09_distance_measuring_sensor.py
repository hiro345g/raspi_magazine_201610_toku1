#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import parts
import math, time

# 定数
HCSR04_TRIG = 19  # トリガーピンのGPIO
HCSR04_ECHO = 26  # エコーーピンのGPIO

hcsr = parts.HcSr04(HCSR04_TRIG, HCSR04_ECHO)
for i in range(5):
    result, v = hcsr.read()
    if result:
        print("distance: {0} [mm]".format(math.floor(v)))
    time.sleep(1)

hcsr.filter('usbwebcam.jpg')
