#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bme280 import bme280, bme280_i2c
import package_parts.bme280_sqlite3 as db
from package_parts import app_12_shelve
import time
import os.path

# - 定数 - #
# BME280用
I2C_ADDRESS = 0x76
I2C_BUS = 1
# DB用
FILE_NAME = '/home/pi/toku1/12-15-a4/bme280_sqlite3.db'
DB_ECHO = False
INTERVAL = 10


def main():
    # 初期処理
    bme280_i2c.set_default_i2c_address(I2C_ADDRESS)
    bme280_i2c.set_default_bus(I2C_BUS)
    bme280.setup()
    app_12_shelve.save_app_data(running=True)
    if os.path.exists(FILE_NAME):
        session = db.start_session(FILE_NAME, DB_ECHO)
    else:
        session = db.start_session_with_createdb(FILE_NAME, DB_ECHO)

    # データの取得
    running = True
    while running:
        data = bme280.read_all()
        air_pressure = db.AirPressure(value=float(data.pressure))
        humidity = db.Humidity(value=float(data.humidity))
        temperature = db.Temperature(value=float(data.temperature))
        session.add(air_pressure)
        session.add(humidity)
        session.add(temperature)
        print('insert:\n\t{0}\n\t{1}\n\t{2}\n'.
              format(str(air_pressure), str(humidity), str(temperature)))
        session.flush()
        session.commit()
        time.sleep(INTERVAL)
        running = app_12_shelve.load_app_data()

    # 終了処理
    session.close()


if __name__ == '__main__':
    main()
