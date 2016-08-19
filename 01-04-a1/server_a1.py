#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import app_server
from package_parts import ht16k33
from package_parts.parts import Led

# -- 定数宣言 -- #
# LEDのGPIO番号
LED_PIN = 4
LED_PINS = [17, 27, 22]
#  LEDマトリクスのパターン
PATTERNS = [
    [
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    [
        0b00111100,
        0b01000010,
        0b10011001,
        0b10100101,
        0b10100101,
        0b10011001,
        0b01000010,
        0b00111100,
    ],
    [
        0b00111100,
        0b01000010,
        0b10000001,
        0b10000001,
        0b10000001,
        0b10000001,
        0b01000010,
        0b00111100,
    ],
    [
        0b10000001,
        0b01000010,
        0b00100100,
        0b00010000,
        0b00001000,
        0b00100100,
        0b01000010,
        0b10000001,
    ],
]
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
<!doctype html>AppA1:success</html>
"""


class Led01(Led):
    """ app_server対応版parts.LEDクラス """

    def exec(self, path):
        """ ルーティング処理を記述 """
        if path.startswith('/led/0?'):
            self.set_status(0)  # LED消灯
        elif path.startswith('/led/1?'):
            self.set_status(1)  # LED点灯
        else:
            return False, ''
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


class LedList:
    """ app_server対応クラス """

    def __init__(self, led_list):
        self.led_list = []
        for pin in led_list:
            self.led_list.append(Led(pin))

    def set_status(self, no):
        if 0 <= no <= len(self.led_list):
            for led in self.led_list:
                led.set_status(0)
            if no > 0:
                self.led_list[no - 1].set_status(1)

    def exec(self, path):
        """ ルーティング処理を記述 """
        print(path)
        if path.startswith('/led_list/0?'):
            self.set_status(0)  # LED消灯
        elif path.startswith('/led_list/1?'):
            self.set_status(1)  # LED1点灯
        elif path.startswith('/led_list/2?'):
            self.set_status(2)  # LED2点灯
        elif path.startswith('/led_list/3?'):
            self.set_status(3)  # LED3点灯
        else:
            return False, ''
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


class MatrixApp:
    """ LEDマトリクス アプリクラス """

    def __init__(self):
        self.address = ht16k33.HT16K33_DEFAULT_ADDRESS
        self.fd = ht16k33.init(self.address)
        self.matrix_data = PATTERNS[0]

    def _matrix_off(self):
        matrix_data = ht16k33.clear(self.fd)
        ht16k33.update(self.fd, matrix_data)

    def _matrix_0(self):
        return self._matrix(0)

    def _matrix(self, id):
        if 0 <= id <= len(PATTERNS):
            self.matrix_data = PATTERNS[id]
            ht16k33.update(self.fd, self.matrix_data)

    def exec(self, path):
        """ ルーティング処理を記述 """
        print(path)
        if path.startswith('/matrix/?'):
            id = 0  # 消灯
        elif path.startswith('/matrix/0?'):
            id = 0  # 消灯
        elif path.startswith('/matrix/1?'):
            id = 1  # バツ
        elif path.startswith('/matrix/2?'):
            id = 2  # マル
        elif path.startswith('/matrix/3?'):
            id = 3  # 二重丸
        else:
            return False, ''
        self._matrix(id)
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


class AppA1:
    def __init__(self):
        led = Led01(LED_PIN)
        led_list = LedList(LED_PINS)
        matrix = MatrixApp()
        self.app_list = []
        self.app_list.append(led)
        self.app_list.append(led_list)
        self.app_list.append(matrix)

    def _pattern0(self):
        self.app_list[0].exec('/led/0?')
        self.app_list[1].exec('/led_list/0?')
        self.app_list[2].exec('/matrix/0?')

    def _pattern1(self):
        self.app_list[0].exec('/led/0?')
        self.app_list[1].exec('/led_list/1?')
        self.app_list[2].exec('/matrix/3?')

    def _pattern2(self):
        self.app_list[0].exec('/led/0?')
        self.app_list[1].exec('/led_list/2?')
        self.app_list[2].exec('/matrix/2?')

    def _pattern3(self):
        self.app_list[0].exec('/led/0?')
        self.app_list[1].exec('/led_list/3?')
        self.app_list[2].exec('/matrix/1?')

    def exec(self, path):
        """ ルーティング処理を記述 """
        print(path)
        if path.startswith('/led_pattern/?'):
            self._pattern0()  # 消灯
        elif path.startswith('/led_pattern/0?'):
            self._pattern0()  # 消灯
        elif path.startswith('/led_pattern/1?'):
            self._pattern1()  # 赤 + バツ
        elif path.startswith('/led_pattern/2?'):
            self._pattern2()  # 黃 + マル
        elif path.startswith('/led_pattern/3?'):
            self._pattern3()  # 緑 + 二重丸
        else:
            # 登録済みアプリクラスのexec()実行
            for app in self.app_list:
                result, result_body = app.exec(path)
                if result:
                    return True, result_body
            # なければこのクラスではサポートしないpath
            return False, ''
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


# 自作のLED01を使ったWebアプリの実行
app = AppA1()
app_server.run(app)
