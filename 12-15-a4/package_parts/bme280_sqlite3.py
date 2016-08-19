# -*- coding: utf-8 -*-
#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import \
    BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
    INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
    VARCHAR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytz import timezone
import datetime


Base = declarative_base()

# - クラス - #
class AirPressure(Base):
    """ 気圧を表すクラス """
    __tablename__ = 'air_pressure'

    id = Column(INTEGER, primary_key=True)
    created_datetime = Column(DATETIME, nullable=False)
    value = Column(FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'AirPressure: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


class Humidity(Base):
    """ 湿度を表すクラス """
    __tablename__ = 'humidity'

    id = Column(INTEGER, primary_key=True)
    created_datetime = Column(DATETIME, nullable=False)
    value = Column(FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'Humidity: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


class Temperature(Base):
    """ 温度を表すクラス """
    __tablename__ = 'temperature'

    id = Column(INTEGER, primary_key=True)
    created_datetime = Column(DATETIME, nullable=False)
    value = Column(FLOAT, nullable=False)

    def __init__(self, value):
        self.created_datetime = datetime.datetime.now(timezone('UTC'))
        self.value = value

    def __repr__(self):
        return 'Temperature: {0}, {1}, {2}'.format(self.id, self.created_datetime, self.value)


# - 関数 - #
def start_session_with_createdb(file_name='appdata.db', echo=False):
    """ データベースの初期化をしながらセッション開始 """
    db_engine = create_engine('sqlite:///' + file_name, echo=echo)
    metadata = Base.metadata
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine)
    return Session()


def start_session(file_name='appdata.db', echo=False):
    """ 既存のデータベースを使ってセッション開始 """
    db_engine = create_engine('sqlite:///' + file_name, echo=echo)
    metadata = Base.metadata
    Session = sessionmaker(bind=db_engine)
    return Session()


def delete_all_data(session):
    """ SQLを直接実行することも可能 """
    result = session.execute("DELETE FROM air_pressure")
    result = session.execute("DELETE FROM temperature")
    result = session.execute("DELETE FROM humidity")
    return result
