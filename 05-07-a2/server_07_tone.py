#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import time, wiringpi

# -- 定数宣言 -- #
SPK_PIN = 5  # 圧電スピーカーのGPIO番号


# -- 関数 -- #
def init():
    """ wiringpiとソフトウェアトーンの初期化 """
    wiringpi.wiringPiSetupGpio()  # wiringpi初期化
    wiringpi.softToneCreate(SPK_PIN)  # ソフトウェアトーン初期化


def play(index):
    """ wiringpiによるソフトウェアトーン再生"""
    melody_list = [
        ((262, 0.5), (294, 0.5), (330, 0.5), (349, 0.5), (392, 0.5), (440, 0.5), (494, 0.5), (525, 0.5)),
        ((525, 0.5), (494, 0.5), (440, 0.5), (392, 0.5), (349, 0.5), (330, 0.5), (294, 0.5), (262, 0.5)),
        ((262, 1), (294, 1), (330, 1), (349, 1), (392, 1), (440, 1), (494, 1), (525, 1)),
    ]
    for v, play_time in melody_list[index]:  # 指定されたメロディーの再生
        wiringpi.softToneWrite(SPK_PIN, v)  # トーン発生
        time.sleep(play_time)  # 同じ音を出力するために処理を遅延
    play_stop()


def play_stop():
    """ 再生終了 """
    wiringpi.softToneWrite(SPK_PIN, 0)  # 再生終了


def shutdown_server():
    """ サーバー停止 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# -- 初期化、 Flaskアプリの用意 -- #
init()
app = Flask(__name__)  # アプリ本体用


# -- ルーティング -- #
@app.route('/speaker/', methods=['GET'])
def speaker():
    """リモート圧電スピーカー用メニュー表示"""
    return render_template('app_07_speaker.html')


@app.route('/speaker/<int:id>', methods=['POST'])
def speaker_play(id):
    """リモート圧電スピーカー再生"""
    play(id)
    return render_template('app_07_speaker.html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    play_stop()
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
