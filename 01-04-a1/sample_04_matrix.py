#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import wiringpi

from package_parts import ht16k33

# -- 変数 -- #
address = ht16k33.HT16K33_DEFAULT_ADDRESS


def main():
    """HT16K33　LEDマトリクス動作確認用メイン処理"""
    matrix_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    fd = ht16k33.init(address)
    # 全ドットを順番に表示
    for r in ht16k33.ROW_ADDRESS:
        for c in ht16k33.COLUMN_VALUES:
            wiringpi.wiringPiI2CWriteReg8(fd, r, c)
            time.sleep(0.1)
            wiringpi.wiringPiI2CWriteReg8(fd, r, c ^ c)  # dot clear
    # クリア
    ht16k33.clear(fd)
    time.sleep(3)
    # (0,0)から(7,7)まで順に点灯
    for i in range(8):
        matrix_data = ht16k33.turn_on_led(fd, i, i, matrix_data)
        ht16k33.update(fd, matrix_data)
        time.sleep(1)
    # (0,0)から(7,7)まで順に消灯
    for i in range(8):
        matrix_data = ht16k33.turn_off_led(fd, i, i, matrix_data)
        ht16k33.update(fd, matrix_data)
        time.sleep(1)
    time.sleep(3)
    # クリア
    ht16k33.clear(fd)


if __name__ == '__main__':
    main()
