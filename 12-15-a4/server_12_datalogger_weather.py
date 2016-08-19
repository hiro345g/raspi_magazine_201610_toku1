#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
from package_parts import app_12_shelve

# - Flaskアプリ -#
app = Flask(__name__)


# - 関数 - #
def shutdown_server():
    """ flaskアプリの停止用 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# - ルーティング - #
@app.route('/')
def root():
    return render_template('app_12.html')


@app.route('/running/0', methods=['POST'])
def datalogger_weather_stop():
    """ datalogger_weathrアプリの停止設定を保存 """
    app_12_shelve.save_app_data(running=False)
    return redirect('/')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
    datalogger_weathrアプリの停止設定も保存
    """
    app_12_shelve.save_app_data(running=False)
    shutdown_server()
    return 'Server shutting down...'
