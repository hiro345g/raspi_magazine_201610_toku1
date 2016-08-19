#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import mjpeg_server, camera, parts
import re

# -- 定数宣言 -- #
HCSR04_TRIG = 19  # トリガーピンのGPIO
HCSR04_ECHO = 26  # エコーーピンのGPIO
SB412A_PIN = 21  # 人感センサーのGPIO
SG90_PIN = 18  # サーボのGPIO
JPEG_FILE_NAME = '/var/ramdisk/08-11-a3/usbwebcam.jpg'  # 画像ファイル名
# HTTPレスポンス用HTMLデータ
HTML_TEXT = """
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>toku1/11 サーボモーター用</title>
    <script>
function servo() {{
  var obj = document.form_servo.select_servo;
  var index = obj.selectedIndex;
  if (index != 0) {{
    location.href = obj.options[index].value;
  }}
  location.href;
}}
    </script>
</head>
<body style="background-color:#ccc">
{0}
<form name="form_servo">
  <select name="select_servo" onchange="servo()" style="width: 60px;">
    <option value="" selected> - </option>
    <option value="/servo/0">0</option>
    <option value="/servo/30">30</option>
    <option value="/servo/60">60</option>
    <option value="/servo/90">90</option>
    <option value="/servo/120">120</option>
    <option value="/servo/150">150</option>
    <option value="/servo/180">180</option>
  </select>
</form>
</body>
</html>
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


def main():
    """ M-JPEG over HTTPサーバー
    人感センサーがオンのときにのみ距離測定
     HCSR-04とSB412Aを組み合わせて
     DistanceMeasuringSenserを作成
     サーボモーターのリモコン機能をServoAppで追加
    """
    filter_obj = DistanceMeasuringSenser(
        parts.HcSr04(HCSR04_TRIG, HCSR04_ECHO),
        parts.Sb412a(SB412A_PIN)
    )
    # カメラオブジェクトの作成
    usbcam = camera.UsbWebCam(file_path=JPEG_FILE_NAME)
    # カメラへフィルター登録
    usbcam.add_filter_app(filter_obj)
    # ServoAppの作成
    servo_app = ServoApp(SG90_PIN)
    # MJPEGサーバーの起動
    mjpeg_server.run(cam=usbcam, app=servo_app)


if __name__ == '__main__':
    main()
