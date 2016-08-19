#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import app_server
from package_parts import ht16k33

# -- 定数宣言 -- #
# LEDマトリクスのパターン
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
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>toku1/04</title>
</head>
<body>
現在の表示:{0}
<ol>
    <li><a href="/matrix/0"><img src="/static/matrix0.png"/></a></li>
    <li><a href="/matrix/1"><img src="/static/matrix1.png"/></a></li>
    <li><a href="/matrix/2"><img src="/static/matrix2.png"/></a></li>
    <li><a href="/matrix/3"><img src="/static/matrix3.png"/></a></li>
</ol>
<p><input type="button" value="停止" onclick="location.href='/shutdown'"></p>
</body>
</html>
"""


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
        if path == '/matrix/':
            id = 0  # 消灯
        elif path == '/matrix/0':
            id = 0  # 消灯
        elif path == '/matrix/1':
            id = 1  # 消灯
        elif path == '/matrix/2':
            id = 2  # 消灯
        elif path == '/matrix/3':
            id = 3  # 消灯
        else:
            return False, ''
        self._matrix(id)
        result_body = self.render_template(id)
        return True, result_body

    def render_template(self, id):
        """ レンダリング処理を記述 """
        return HTML_TEXT.format(id)


# 自作のMatrixAppを使ったWebアプリの実行
app = MatrixApp()
app_server.run(app)
