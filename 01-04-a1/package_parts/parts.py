#
# -*- coding: utf-8 -*-
import wiringpi


class Led:
    """ LED用クラス """

    def __init__(self, pin):
        """ 初期化メソッド """
        self.pin = to_wiringpi_pin(pin)  # LED用のGPIOピン
        self.status = wiringpi.LOW  # LED用
        # GPIOとLEDの初期化
        wiringpi.pinMode(self.pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self.pin, self.status)

    def get_status(self):
        """ LEDの状態を返却 """
        return self.status

    def set_status(self, value):
        """ LEDの点灯・消灯と状態の保存。
           valueが1のとき点灯
           valueが0のとき消灯
        """
        self.status = value
        wiringpi.digitalWrite(self.pin, self.status)


def to_wiringpi_pin(bcm_pin):
    """ BCMのピンからwiringPiのピンを取得
    ht16k33.pyを使う場合
    wiringpi.wiringPiSetup()を使うため
    wiringpi.wiringPiSetupGpio()が使えない。
    このため、BCMピンの番号をwiringPiのピン番号へ変換する必要がある
    """
    pin_map = {
        17: 0,
        18: 1,
        27: 2,
        22: 3,
        23: 4,
        24: 5,
        25: 6,
        4: 7,
        2: 8,
        3: 9,
        8: 10,
        7: 11,
        10: 12,
        9: 13,
        11: 14,
        14: 15,
        15: 16,
        28: 17,
        29: 18,
        30: 19,
        31: 20,
        5: 21,
        6: 22,
        13: 23,
        19: 24,
        26: 25,
        12: 26,
        16: 27,
        20: 28,
        21: 29,
        0: 30,
        1: 31,
    }
    return pin_map[bcm_pin]
