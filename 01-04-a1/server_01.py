#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import app_server
from package_parts.parts import Led

# -- 定数宣言 -- #
# LEDのGPIO番号
LED_PIN = 4
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>toku1/01</title>
</head>
<body>
<p><input type="button" value="点灯" onclick="location.href='/led/1'"></p>
<p><input type="button" value="消灯" onclick="location.href='/led/0'"></p>
<p><input type="button" value="停止" onclick="location.href='/shutdown'"></p>
</body>
</html>
"""


class Led01(Led):
    """ app_server対応版parts.LEDクラス """

    def exec(self, path):
        """ ルーティング処理を記述 """
        if path == '/led/0':
            self.set_status(0)  # LED消灯
        elif path == '/led/1':
            self.set_status(1)  # LED点灯
        else:
            return False, ''
        result_body = self.render_template()
        return True, result_body

    def render_template(self):
        """ レンダリング処理を記述 """
        return HTML_TEXT

# 自作のLED01を使ったWebアプリの実行
app = Led01(LED_PIN)
app_server.run(app)
