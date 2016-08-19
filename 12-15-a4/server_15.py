#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

# - Flaskアプリ -#
app = Flask(__name__)
app.config.from_pyfile('server_15.cfg')
data_dict = {}


# - 関数 - #
def shutdown_server():
    """ flaskアプリの停止用 """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def check(http_request):
    if not http_request.is_xhr:  # XMLHttpRequestによるリクエストならis_xhrはTrue
        print("not request.is_xhr")
        for h in request.headers:
            print("header: " + str(h))
        return False, jsonify(res='fail'), 406
    if http_request.headers['Content-Type'] != 'application/json':
        print(http_request.headers['Content-Type'])
        return False, jsonify(res='fail'), 406
    return True, '', 200


# - ルーティング - #
@app.route('/', methods=['GET'])
def document_root():
    return 'server_15'


@app.route('/api/data/<int:id>', methods=['GET'])
def api_read(id):
    global data_dict
    result, response, response_code = check(request)
    if not result:
        return response, response_code
    if id in data_dict:
        r = jsonify(res='ok', value=data_dict[id])
        print(r)
        return r
    else:
        return jsonify(res='fail')


@app.route('/api/data/<int:id>', methods=['POST'])
def api_create(id):
    global data_dict
    result, response, response_code = check(request)
    if not result:
        return response, response_code
    for e in request.json:
        print('request.json e:(' + e + ', ' + request.json[e] + ')')
    if id in data_dict:
        return jsonify(res='fail'), 400
    else:
        data_dict[id] = request.json['value']
        return jsonify(res='ok'), 201


@app.route('/api/data/<int:id>', methods=['PUT'])
def apid_update(id):
    global data_dict
    result, response, response_code = check(request)
    if not result:
        return response, response_code
    for e in request.json:
        print('request.json e:(' + e + ', ' + request.json[e] + ')')
    if id in data_dict:
        data_dict[id] = request.json['value']
        return jsonify(res='ok')
    else:
        return jsonify(res='fail'), 400


@app.route('/api/data/<int:id>', methods=['DELETE'])
def api_delete(id):
    global data_dict
    result, response, response_code = check(request)
    if not result:
        return response, response_code
    if id in data_dict:
        print('delete:' + str(id))
        data_dict.pop(id, None)
        return '', 204
    else:
        return jsonify(res='fail'), 404


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ flaskアプリの停止
    """
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Flaskアプリの起動
