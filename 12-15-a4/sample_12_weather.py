#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bme280 import bme280, bme280_i2c

# 定数
I2C_ADDRESS = 0x76
I2C_BUS = 1

# 初期設定
bme280_i2c.set_default_i2c_address(I2C_ADDRESS)
bme280_i2c.set_default_bus(I2C_BUS)
bme280.setup()

# データの取得と表示
data = bme280.read_all()
print('bme280')
print("\t{0:7.2f} hPa".format(data.pressure))
print("\t{0:7.2f} ％".format(data.humidity))
print("\t{0:7.2f} C".format(data.temperature))
