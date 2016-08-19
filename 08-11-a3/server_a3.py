#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import mjpeg_server, camera, parts
from package_parts.parts import HcSr04
import re, shutil

# -- 定数宣言 -- #
HCSR04_TRIG = 19  # トリガーピンのGPIO
HCSR04_ECHO = 26  # エコーーピンのGPIO
SB412A_PIN = 21  # 人感センサーのGPIO
SG90_PIN = 18  # サーボのGPIO
JPEG_FILE_NAME = '/var/ramdisk/08-11-a3/usbwebcam.jpg'  # 画像ファイル名
PHOTO_FILE_NAME = './static/100mm_photo.jpg'
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
{0}
"""


class DistanceMeasuringSenser:
    """ 人感センサーがオンのときにのみ距離測定をする距離センサークラス """

    def __init__(self, distance_measuring_sensor, motion_detector):
        """ 初期化処理 """
        self.distance_measuring_sensor = distance_measuring_sensor
        self.motion_detector = motion_detector

    def filter(self, src_file_name):
        """ フィルター処理 人感センサーがオンのときにのみ距離測定 """
        if not self.motion_detector.is_on():
            return
        self.distance_measuring_sensor.filter(src_file_name)


class ServoApp(parts.Sg90):
    """ parts.Sg90のmjpeg_server対応版クラス """

    def exec(self, path):
        """ ルーティング処理を記述 """
        if not path.startswith('/servo/'):
            return False, ''
        servo_path = path.replace('/servo', '')
        if servo_path == '/':
            servo_degree = "None"
        else:
            m = re.search(r'\d{1,3}', servo_path)
            if m:
                degree = int(m.group(0))
                servo_degree = "Servo: {0} 度".format(degree)
                self.set_position(degree)  # サーボ設定
            else:
                # 3桁以内の数字ではないのでエラー
                return False, ''
        result_body = self._render_template(servo_degree)
        return True, result_body

    def _render_template(self, servo_degree):
        """ レンダリング処理を記述 """
        return HTML_TEXT.format(servo_degree)


class PhotoSaver:
    """ 人感センサーがオンのときにのみ距離測定をする距離センサークラス """

    def __init__(self, distance_measuring_sensor):
        """ 初期化処理 """
        self.distance_measuring_sensor = distance_measuring_sensor
        self.cnt = 0

    def filter(self, src_file_name):
        """ 距離が100未満なら写真保存 """
        result, distance = self.distance_measuring_sensor.read()
        if result and distance < 100:
            self.cnt += 1
            if 30 < self.cnt :  # 検知回数が連続30回を超えたら写真保存
                shutil.copy(src_file_name, PHOTO_FILE_NAME)
                self.cnt = 0
        else:
            self.cnt = 0


def main():
    """ M-JPEG over HTTPサーバー
    人感センサーがオンのときにのみ距離測定
     HCSR-04とSB412Aを組み合わせて
     DistanceMeasuringSenserを作成
     サーボモーターのリモコン機能をServoAppで追加
     自動撮影機能をPhotoSaverで追加
    """
    # カメラオブジェクトの作成
    usbcam = camera.UsbWebCam(file_path=JPEG_FILE_NAME)
    hcsr = HcSr04(HCSR04_TRIG, HCSR04_ECHO)
    filter_obj = PhotoSaver(hcsr)
    usbcam.add_filter_app(filter_obj)
    filter_obj = DistanceMeasuringSenser(
        hcsr,
        parts.Sb412a(SB412A_PIN)
    )
    # カメラへフィルター登録
    usbcam.add_filter_app(filter_obj)
    # ServoAppの作成
    servo_app = ServoApp(SG90_PIN)
    # MJPEGサーバーの起動
    mjpeg_server.run(cam=usbcam, app=servo_app)


if __name__ == '__main__':
    main()
