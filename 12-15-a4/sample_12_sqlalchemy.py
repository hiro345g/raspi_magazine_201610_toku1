#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import package_parts.bme280_sqlite3 as db
from pytz import timezone
import datetime

file_name = 'sample_12.db'
echo = True

# データベースを作成しながらセッションを開始
# echo は False にして結果だけ表示
echo = False
session = db.start_session_with_createdb(file_name, echo)

# サンプルデータの追加
current_time = datetime.datetime.now(timezone('UTC'))
for i in [40, 30, 20, 10, 0]:
    ap = db.AirPressure(value=1.2)
    ap.created_datetime = current_time - datetime.timedelta(minutes=i)
    session.add(ap)
session.flush()
session.commit()

print('SQLAlchemy')

# 最初のデータ
air_pressure = session.query(db.AirPressure).first()
print('\tfirst:' + str(air_pressure))

# 全部
air_pressure_list = session.query(db.AirPressure).all()
for entry in air_pressure_list:
    print('\tall: ' + str(entry))

# id指定
air_pressure_list = session.query(db.AirPressure).filter_by(id=2).all()
for entry in air_pressure_list:
    print('\tid=2:' + str(entry))

# 期間指定
start_time = (current_time - datetime.timedelta(minutes=15))
end_time = (current_time - datetime.timedelta(minutes=5))
air_pressure_list = session.query(db.AirPressure).filter(
    db.AirPressure.created_datetime.between(start_time, end_time)).all()
print('\t{0} - {1}:'.format(start_time, end_time))
for entry in air_pressure_list:
    print('\t\t' + str(entry))

# データの全削除
for entry in air_pressure_list:
    session.delete(entry)
session.commit()

# セッション終了
session.close()
