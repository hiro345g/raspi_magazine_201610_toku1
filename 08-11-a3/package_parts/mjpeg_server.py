#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import os, time

# グローバル変数
_cam = None  # カメラ用
_running_mjpeg_server = False  # サーバ実行制御用
_server = None  # サーバー停止用
_application = None  # アプリ機能拡張用


class Handler(BaseHTTPRequestHandler):
    """ HTTPリクエストを処理するためのハンドラクラス """

    def do_GET(self):
        """ GETメソッドのHTTPリクエスト処理用 """
        global _running_mjpeg_server
        global _server
        global _application
        url_path = self.path
        if self.path == '/':
            # '/' はデフォルトで '/index.html' を返す
            url_path = '/index.html'
        if url_path == '/shutdown':
            # 停止
            self._shutdown()
            return
        if url_path == '/cam.mjpg':
            # MJPEG
            self._mjpeg_run()
            return
        if _application is not None:
            # アプリケーション拡張機能がある場合は実行
            result, response_body = _application.exec(url_path)
            if result:
                # 成功なら返却された文字列を返して終了
                self._do_text_response(response_body)
                return
        try:
            result = self._do_file_response(url_path)
            if not result:
                # 処理がされなかったurl_pathはリソースが見つからなかったため404エラー
                self.send_error(404, 'File Not Found: {0}'.format(url_path))
        except IOError:
            self.send_error(404, 'File Not Found: {0}'.format(url_path))
        return

    def _shutdown(self):
        """ 停止のための処理 """
        global _cam
        global _running_mjpeg_server
        global _server
        _running_mjpeg_server = False
        mime_type = 'text/html; charset=utf-8'
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()
        self.wfile.write(bytes('shutdown cam.mjpg', 'utf-8'))
        if _cam is not None:
            _cam.stop()
            _cam = None
        if _server is not None and _server.socket is not None:
            _server.socket.close()
            _server = None

    def _mjpeg_run(self):
        """ MJPEGサーバー機能提供のための処理 """
        global _cam
        global _running_mjpeg_server
        global _server
        if _running_mjpeg_server:
            if _cam is not None:
                _cam.stop()
        _running_mjpeg_server = True
        mime_type = 'multipart/x-mixed-replace; boundary=--jpgboundary'
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()
        if _cam is not None:
            _cam.start()
        else:
            return
        file_path = _cam.file_path
        while _running_mjpeg_server:
            try:
                _cam.capture()
                self.wfile.write('--jpgboundary\r\n'.encode('utf-8'))
                self.wfile.flush()
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', os.path.getsize(file_path))
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            except IOError:
                print('mjpeg IOError')
                break
            except KeyboardInterrupt:
                print('mjpeg KeyboardInterrupt')
                break
        if _cam is not None:
            _cam.stop()
        if not _running_mjpeg_server:
            if _server is not None and _server.socket is not None:
                _server.socket.close()
                _server = None

    def _do_file_response(self, request_path):
        """ HTML, JPEGファイル用の処理 """
        parse_result = urllib.parse.urlparse(request_path)  # 戻り値がurllib.parse.ParseResultオブジェクト
        url_path = parse_result.path
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

    def _do_text_response(self, s):
        """ HTML文字列返却用 """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(s, 'utf-8'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """スレッドでリクエストを処理"""


def run(host='0.0.0.0', port=8081, cam=None, app=None):
    """ サーバー起動用関数
    host: 待機するIPアドレス
    port: 待機するポート
    cam: mjpeg_server用カメラオブジェクト start(), stop(), capture() メソッドが必要
    app: アプリケーション機能拡張用オブジェクト exec()メソッドが必要
    """
    global _application
    global _cam
    global _server
    _application = app
    _cam = cam
    _server = ThreadedHTTPServer((host, port), Handler)
    print(time.asctime(), 'Server start - {0}:{1}'.format(host, port))
    try:
        _server.serve_forever()
    except ValueError:
        print('remote shutdown')
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        if _cam is not None:
            _cam.stop()
        if _server is not None and _server.socket is not None:
            _server.socket.close()
    print(time.asctime(), 'Server stop - {0}:{1}'.format(host, port))


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    run()
