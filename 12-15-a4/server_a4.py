#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import app_12_shelve
from flask import Flask, redirect, request

# - Flaskアプリ -#
app = Flask(__name__)
app.config.from_pyfile('server_a4.cfg')


# - 関数 - #
def shutdown_server():
    """ flaskアプリの停止用 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# - ルーティング - #
@app.route('/running/0', methods=['POST'])
def datalogger_weather_stop():
    """ datalogger_weathrアプリの停止設定を保存 """
    app_12_shelve.save_app_data(running=False)
    return redirect('/static/app_a4.html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
    """
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Flaskアプリの起動
