#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package_parts import mjpeg_server, camera

JPEG_FILE_NAME = '/var/ramdisk/08-11-a3/usbwebcam.jpg'  # 画像ファイル名


def main():
    """ M-JPEG over HTTPサーバー
    """
    # カメラオブジェクトの作成
    usbcam = camera.UsbWebCam(file_path=JPEG_FILE_NAME)
    # サーバーの起動
    mjpeg_server.run(cam=usbcam)


if __name__ == '__main__':
    main()
