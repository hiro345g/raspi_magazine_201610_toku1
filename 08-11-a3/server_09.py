#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import mjpeg_server, camera, parts

# 定数
HCSR04_TRIG = 19  # トリガーピンのGPIO
HCSR04_ECHO = 26  # エコーーピンのGPIO
JPEG_FILE_NAME = '/var/ramdisk/08-11-a3/usbwebcam.jpg'  # 画像ファイル名


def main():
    """ M-JPEG over HTTPサーバー
    """
    # 距離センサーオブジェクト作成
    hcsr = parts.HcSr04(HCSR04_TRIG, HCSR04_ECHO)
    # カメラオブジェクトの作成
    usbcam = camera.UsbWebCam(file_path=JPEG_FILE_NAME)
    # 距離センサーを使った画像合成フィルター登録
    usbcam.add_filter_app(hcsr)
    # サーバーの起動
    mjpeg_server.run(cam=usbcam)


if __name__ == '__main__':
    main()
