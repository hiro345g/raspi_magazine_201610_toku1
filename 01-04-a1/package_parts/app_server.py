#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, time

# グローバル変数
_application = None
_server = None


class Handler(BaseHTTPRequestHandler):
    """ HTTPリクエストを処理するクラス """

    def do_GET(self):
        """ GETメソッドによるHTTPリクエストを処理する関数 """
        global _application
        if self.path == '/shutdown':
            self._do_response('shutdown')
            global _server
            if _server is not None and _server.socket is not None:
                _server.socket.close()
                _server = None
                return
        if _application is not None:
            result, response_body = _application.exec(self.path)
        if result:
            self._do_response(response_body)
        else:
            result = self._do_file_response(self.path)
            if not result: # 上記にあてはまらない場合は対応するパスがない
                self.send_error(404, 'File Not Found: {0}'.format(self.path))
        return

    def _do_response(self, s):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(s, 'utf-8'))

    def _do_file_response(self, url_path):
        """ HTML, JPEGファイル用の処理 """
        send_reply = False
        if url_path.endswith('.css'):
            mime_type = 'text/css'
            send_reply = True
        if url_path.endswith('.html'):
            mime_type = 'text/html; charset=utf-8'
            send_reply = True
        if url_path.endswith('.js'):
            mime_type = 'text/javascript'
            send_reply = True
        if url_path.endswith('.jpg'):
            mime_type = 'image/jpg'
            send_reply = True
        if url_path.endswith('.png'):
            mime_type = 'image/png'
            send_reply = True
        if send_reply:
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()
            f = os.path.abspath('./{0}'.format(url_path.replace('..', '')))
            if mime_type.startswith('text'):
                with open(f, 'r') as file:
                    self.wfile.write(bytes(file.read(), 'utf-8'))
            else:
                with open(f, 'rb') as file:
                    self.wfile.write(file.read())
        return send_reply


def run(app=None, host='0.0.0.0', port=8080, cam=None):
    """ サーバー起動用関数
    app: アプリケーション機能拡張用オブジェクト exec()メソッドが必要
    host: 待機するIPアドレス
    port: 待機するポート
    cam: mjpeg_server用カメラオブジェクト start(), stop(), capture() メソッドが必要
    """
    global _application
    global _server
    _application = app
    _server = HTTPServer((host, port), Handler)
    print(time.asctime(), 'Server start - {0}:{1}'.format(host, port))
    try:
        _server.serve_forever()
    except ValueError:
        print('remote shutdown')
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        if _server is not None and _server.socket is not None:
            _server.socket.close()
    print(time.asctime(), 'Server stop - {0}:{1}'.format(host, port))


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    run()
