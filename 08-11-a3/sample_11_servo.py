#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import parts
import time

SG90_PIN = 18
degrees = [0, 30, 60, 90, 120, 150, 180]
servo = parts.Sg90(SG90_PIN)
for degree in degrees:
    print('degree:' + str(degree))
    servo.set_position(degree)
    time.sleep(3)
