#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, requests, json

headers = {
    'User-Agent': 'client_15.py',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}
host_url = 'http://127.0.0.1:5001'


def get_root():
    url = host_url + '/'
    response = requests.get(url, headers=headers)
    print(response.text)
    time.sleep(1)


def get():
    url = host_url + '/api/data/1'
    response = requests.get(url, headers=headers)
    print(response.text)


def post():
    url = host_url + '/api/data/1'
    json_data = {'value': '34.5'}
    print(json.dumps(json_data))
    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    print(response.text)


def put():
    url = host_url + '/api/data/1'
    json_data = {'value': '67.8'}
    response = requests.put(url, data=json.dumps(json_data), headers=headers)
    print(response.text)


def delete():
    url = host_url + '/api/data/1'
    json_data = {'value': ''}
    response = requests.delete(url, data=json.dumps(json_data), headers=headers)
    print(response.text)


def main():
    print('ドキュメントルートのデータ取得 ----')
    get_root()
    print('データがないことを確認 ----')
    get()
    print('データ追加 ----')
    post()
    print('データ追加確認 ----')
    get()
    print('同じidのデータ追加はできない ----')
    post()
    print('データ更新 ----')
    put()
    print('データ更新確認 ----')
    get()
    print('データ削除 ----')
    delete()
    print('データ削除確認 ----')
    get()


if __name__ == '__main__':
    main()
