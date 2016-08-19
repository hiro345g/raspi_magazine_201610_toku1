#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import mjpeg_server, camera, parts

# 定数
HCSR04_TRIG = 19  # トリガーピンのGPIO
HCSR04_ECHO = 26  # エコーーピンのGPIO
SB412A_PIN = 21  # 人感センサーのGPIO
JPEG_FILE_NAME = '/var/ramdisk/08-11-a3/usbwebcam.jpg'  # 画像ファイル名


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


def main():
    """ M-JPEG over HTTPサーバー
    人感センサーがオンのときにのみ距離測定
     HCSR-04とSB412Aを組み合わせて
     DistanceMeasuringSenserを作成
    """
    filter_obj = DistanceMeasuringSenser(
        parts.HcSr04(HCSR04_TRIG, HCSR04_ECHO),
        parts.Sb412a(SB412A_PIN)
    )
    # カメラオブジェクトの作成
    usbcam = camera.UsbWebCam(file_path=JPEG_FILE_NAME)
    # カメラへフィルター登録
    usbcam.add_filter_app(filter_obj)
    # サーバーの起動
    mjpeg_server.run(cam=usbcam)


if __name__ == '__main__':
    main()