#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import subprocess


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
@app.route('/', methods=['GET'])
def document_root():
    """タイマーメニュー表示"""
    return render_template('app_a2.html')


@app.route('/timer_start/', methods=['POST'])
def timer_start():
    """タイマーコマンドの実行"""
    if 'seconds' in request.form:
        s = int(request.form['seconds'])
        cmds = ['sh', './run_a2_app.sh', str(s)]  # コマンドリストの作成
        returncode = subprocess.call(cmds)  # コマンドの呼び出し
        print("{0} {1} {2} : {3}".format(cmds[0], cmds[1], cmds[2], str(returncode)))  # コマンドの結果出力
    return render_template('app_a2.html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
    """
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    app.run(host='0.0.0.0')
