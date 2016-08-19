#!/usr/bin/env python
# -*- coding: utf-8 -*-
import app_03_db
from package_parts import app_server

# -- 定数宣言 -- #
# LEDのGPIO番号
LED_PINS = [17, 27, 22]
# PWMの範囲
LED_PWM_RANGE = 100
# 処理継続用
CONTINUE = True
# 処理停止用
STOP = False
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>toku1/02</title>
    <meta http-equiv="refresh" content="0;URL=/static/led_pwm_list.html">
</head>
<body>
</body>
</html>
"""


class PwmLedList:
    """ app_server対応クラス """

    def __init__(self):
        self.running = True
        self.led_values = [0, 0, 0]
        app_03_db.save_led_pwm_list(self.running, self.led_values)

    def exec(self, path):
        """ ルーティング処理を記述 """
        print(path)
        # self.led_valuesを使うときはindexは0以上。-1のままなら使わない
        index = -1
        if path.startswith('/led_pwm_list/0/1?'):
            self.running = True
        elif path.startswith('/led_pwm_list/0/0?'):
            self.running = False
        elif path.startswith('/led_pwm_list/1/'):
            index = 0
            pos = path.find('?') # ?の位置を取得
            if pos < -1:
                pos = len(path) # ?がないときはpathの長さ
            v = int(path[16:pos]) # /led_pwm_list/1/<v> の<v>を取得
        elif path.startswith('/led_pwm_list/2/'):
            index = 1
            pos = path.find('?')
            if pos < -1:
                pos = len(path)
            v = int(path[16:pos])
        elif path.startswith('/led_pwm_list/3/'):
            index = 2
            pos = path.find('?')
            if pos < -1:
                pos = len(path)
            v = int(path[16:pos])
        else:
            return False, ''
        if index >= 0:
            if v < 0:
                v = 0
            if v > 100:
                v = 100
            self.led_values[index] = v
        app_03_db.save_led_pwm_list(self.running, self.led_values)
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT


# 自作のPwmLedListを使ったWebアプリの実行
app = PwmLedList()
app_server.run(app)
