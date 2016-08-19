#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
import app_05_db


# -- 関数 -- #
def shutdown_server():
    """ サーバー停止 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# -- 初期化、 Flaskアプリの用意 -- #
app = Flask(__name__)  # アプリ本体用


# -- ルーティング -- #
@app.route('/status/led', methods=['GET'])
def status_led():
    """LEDの状態を取得"""
    running, led_values, button_values = app_05_db.load_app_05_status()
    if not running:
        return 'not running', 404
    return str(led_values[0])


@app.route('/status/button', methods=['GET'])
def status_button():
    """ボタンの状態を取得"""
    running, led_values, button_values = app_05_db.load_app_05_status()
    if not running:
        return 'not running', 404
    return str(button_values[0])


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """ flaskアプリとapp_05の停止
      app_05.dbの排他制御をしていないので、
      ボタンの状態を変更しながら停止しないこと
    """
    running, led_values, button_values = app_05_db.load_app_05_status()
    running = False
    app_05_db.save_app_05_status(running, led_values, button_values)
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    app.run(host='0.0.0.0')
