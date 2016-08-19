#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import package_parts.bme280_sqlite3 as db

# - 定数 - #
I2C_ADDRESS = 0x76
I2C_BUS = 1
INTERVAL = 10
FILE_NAME = '/home/pi/toku1/12-15-a4/bme280_sqlite3.db'
DB_ECHO = False


def main():
    session = db.start_session(FILE_NAME, DB_ECHO)
    air_pressure_list = session.query(db.AirPressure).all()
    print('air_pressure')
    for entry in air_pressure_list:
        print('\t' + str(entry))
    humidity_list = session.query(db.Humidity).all()
    print('humidity')
    for entry in humidity_list:
        print('\t' + str(entry))
    temperature_list = session.query(db.Temperature).all()
    print('temperature')
    for entry in temperature_list:
        print('\t' + str(entry))
    # 終了処理
    session.close()


if __name__ == '__main__':
    main()
