#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
import datetime

# - Flaskアプリ -#
app = Flask(__name__)
app.config.from_pyfile('server_13_bme280.cfg')
db = SQLAlchemy(app)


# - クラス - #
# flask_sqlalchemyの機能を使っているため、SQLAlchemyをそのまま
# 使う場合とは記述が違っている点に注意
class AirPressure(db.Model):
    """ 気圧を表すクラス """
    __tablename__ = 'air_pressure'

    id = db.Column(db.INTEGER, primary_key=True)
    created_datetime = db.Column(db.DATETIME, nullable=False)
    value = db.Column(db.FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'AirPressure: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


class Humidity(db.Model):
    """ 湿度を表すクラス """
    __tablename__ = 'humidity'

    id = db.Column(db.INTEGER, primary_key=True)
    created_datetime = db.Column(db.DATETIME, nullable=False)
    value = db.Column(db.FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'Humidity: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


class Temperature(db.Model):
    """ 温度を表すクラス """
    __tablename__ = 'temperature'

    id = db.Column(db.INTEGER, primary_key=True)
    created_datetime = db.Column(db.DATETIME, nullable=False)
    value = db.Column(db.FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'Temperature: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


# - 関数 - #
def shutdown_server():
    """ flaskアプリの停止用 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def query_1():
    """ 1時間のデータを対象 """
    print("query_1()")
    current_time = datetime.datetime.now(timezone('UTC'))
    start_time = (current_time - datetime.timedelta(hours=1))
    end_time = current_time
    air_pressure_data = AirPressure.query.filter(
        AirPressure.created_datetime.between(start_time, end_time)).order_by(
        AirPressure.id.asc()).all()
    air_pressure_list = []
    for entry in air_pressure_data:
        air_pressure_list.append(to_dict(entry))
    return air_pressure_list


def to_dict(item):
    d = {}
    d['id'] = item.id
    d['created_datetime'] = to_jst(item.created_datetime)
    d['value'] = item.value
    return d


def to_jst(utc_now):
    jst_format = '%Y-%m-%d %H:%M:%S %Z%z'
    tz_tokyo = timezone('Asia/Tokyo')
    return tz_tokyo.fromutc(utc_now).strftime(jst_format)


# - ルーティング - #
@app.route('/')
def show_all():
    """ すべてのデータを表示 """
    air_pressure_data = AirPressure.query.order_by(AirPressure.created_datetime.asc()).all()
    air_pressure_list = []
    for entry in air_pressure_data:
        air_pressure_list.append(to_dict(entry))
    return render_template('app_13.html', air_pressure_list=air_pressure_list)


@app.route('/1')
def show_1():
    """ 1時間前までのデータを表示 """
    air_pressure_list = query_1()
    return render_template('app_13.html', air_pressure_list=air_pressure_list)


@app.route('/json/1')
def json_1():
    """ 1時間前までのデータをJSONで返却 """
    air_pressure_list = query_1()
    results = {"air_pressure_list": air_pressure_list}
    return jsonify(results)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
    """
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Flaskアプリの起動
