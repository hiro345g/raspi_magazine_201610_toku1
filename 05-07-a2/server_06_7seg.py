#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from package_parts import ht16k33_7seg


# -- 関数 -- #
def init():
    address = ht16k33_7seg.HT16K33_DEFAULT_ADDRESS
    fd = ht16k33_7seg.init(address)
    return fd


def led_off():
    """ 7セグLED消灯 """
    global fd
    data = ht16k33_7seg.clear(fd)
    ht16k33_7seg.update(fd, data)


def led_num(num):
    """ 7セグLED表示 """
    global fd
    data = [0x00, 0x00, 0x00, 0x00]
    n = '{0:04d}'.format(num)
    for index, c in enumerate(list(n)):
        data[index] = ht16k33_7seg.get_font(c)
    ht16k33_7seg.update(fd, data)


def shutdown_server():
    """ サーバー停止 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# 初期化とFlaskアプリの実行
fd = init()
app = Flask(__name__)  # アプリ本体用


# -- ルーティング -- #
@app.route('/seven_led/', methods=['GET'])
def seven_led():
    """リモート7セグLED用メニュー表示"""
    return render_template('app_06_7seg.html')


@app.route('/seven_led/', methods=['POST'])
def seven_led_post():
    """ 指定された数字を7SEG LEDで表示 """
    if 'seven_seg_number' in request.form:
        i = int(request.form['seven_seg_number'])
        led_num(i)
        n = '{0:04d}'.format(i)
        return render_template('app_06_7seg.html', seven_seg_number=n)
    else:
        return render_template('app_06_7seg.html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
     7SEG LEDも消灯
    """
    led_off()
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    app.run(host='0.0.0.0')
