#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import app_server
from package_parts.parts import Led

# -- 定数宣言 -- #
# LEDのGPIO番号
LED_PINS = [17, 27, 22]  # LEDのGPIO番号
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>toku1/02</title>
</head>
<body>
<form>
    <p><label><input type="radio" name="led_checkbox" onclick="location.href='/led_list/0'">消灯</label></p>
    <p><label><input type="radio" name="led_checkbox" onclick="location.href='/led_list/1'">LED1 点灯</label></p>
    <p><label><input type="radio" name="led_checkbox" onclick="location.href='/led_list/2'">LED2 点灯</label></p>
    <p><label><input type="radio" name="led_checkbox" onclick="location.href='/led_list/3'">LED3 点灯</label></p>
</form>
<p><input type="button" value="停止" onclick="location.href='/shutdown'"></p>
</body>
</html>
"""


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
        if path == '/led_list/0':
            self.set_status(0)  # LED消灯
        elif path == '/led_list/1':
            self.set_status(1)  # LED1点灯
        elif path == '/led_list/2':
            self.set_status(2)  # LED2点灯
        elif path == '/led_list/3':
            self.set_status(3)  # LED3点灯
        else:
            return False, ''
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


# 自作のLedListを使ったWebアプリの実行
app = LedList(LED_PINS)
app_server.run(app)
