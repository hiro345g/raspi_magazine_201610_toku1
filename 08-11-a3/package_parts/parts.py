# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import math, time, wiringpi


class HcSr04:
    """ HC-SR04アプリケーション用クラス """
    PULSE_TRIGGER = 0.00001  # 10 μsec
    SPEED_OF_SOUND = 340  # 340 m/sec
    PULSE_TRIGGER_INTERVAL = 0.06  # 60 msec
    TIMEOUT = 2 * 180 * 0.01 / SPEED_OF_SOUND  # 約 0.0106 sec

    def __init__(self, trig, echo):
        """ 初期化メソッド """
        self.trig = trig  # Trig用のGPIOピン
        self.echo = echo  # Echo用のGPIOピン
        # GPIOの初期化
        wiringpi.pinMode(self.trig, wiringpi.OUTPUT)
        wiringpi.pinMode(self.echo, wiringpi.INPUT)
        wiringpi.digitalWrite(self.trig, wiringpi.LOW)
        time.sleep(1)

    def wait_for_echo(self, wait_value, wait_time):
        """ エコーピンの値がwait_valueで指定した値になるまで取得し続けます。
        ただし、wait_timeを過ぎたら終了します。
        wait_valueで指定した値になった時刻と、時刻取得成功判定用の結果を返します。
        時刻取得成功判定用の結果は成功ならTrue、失敗ならFalseとなります。
       """
        timeout = False
        start_time = time.time()
        current_time = start_time
        while wiringpi.digitalRead(self.echo) != wait_value:
            current_time = time.time()
            timeout = (current_time - start_time) > wait_time
            if timeout is True:
                break
        return current_time, not timeout

    def read(self):
        """ HC-SR04から距離を取得する関数です。
        距離取得成功判定用の結果と測定距離を返します。
        距離取得成功判定用の結果は成功ならTrue、失敗ならFalseとなります。
        距離は[mm]となります。
        """
        time.sleep(self.PULSE_TRIGGER_INTERVAL)
        # トリガー信号を発信
        wiringpi.digitalWrite(self.trig, wiringpi.HIGH)
        time.sleep(self.PULSE_TRIGGER)
        wiringpi.digitalWrite(self.trig, wiringpi.LOW)
        start_time, echo_result = self.wait_for_echo(wiringpi.HIGH, self.TIMEOUT)
        if echo_result:
            end_time, echo_result = self.wait_for_echo(wiringpi.LOW, self.TIMEOUT)
            if echo_result:
                return True, (end_time - start_time) * (self.SPEED_OF_SOUND * 1000 / 2)
            else:
                print("wait_for_echo(GPIO.HIGH) error")
        else:
            print("wait_for_echo(GPIO.LOW) error")
        return False, 0

    def filter(self, src_file_name):
        result, v = self.read()
        if result:
            img = Image.open(src_file_name)
            text = "distance: {0} [mm]".format(math.floor(v))
            draw = ImageDraw.Draw(img)
            draw.rectangle((10, 10, 300, 34), fill=(255, 255, 255))
            draw.font = ImageFont.truetype(
                "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 24)
            pos = (15, 10)
            text_color = (0, 0, 0)
            draw.text(pos, text, text_color)
            img.save(src_file_name)


class Sb412a:
    """ SB412Aセンサー用クラス (作成時にSB412AをSBA12Aと見間違えたため、クラス名がSba12aとなっている) """

    def __init__(self, pin):
        """ 初期化メソッド """
        self.pin = pin  # GPIOピン
        # GPIOの初期化
        wiringpi.pinMode(self.pin, wiringpi.INPUT)

    def is_on(self):
        """ 人感センサーに反応がある時 True、ない時 False """
        return wiringpi.digitalRead(self.pin) == wiringpi.HIGH


class Sg90:
    """ SG90サーボモーター用クラス """
    PWM_CLOCK = 375

    def __init__(self, pin):
        """ 初期化メソッド """
        self.pin = pin  # GPIOピン
        # GPIOの初期化
        wiringpi.pinMode(self.pin, wiringpi.PWM_OUTPUT)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetRange(1024)
        wiringpi.pwmSetClock(self.PWM_CLOCK)

    def set_position(self, degree):
        """ 角度を度数で受け取って指定位置まで回転
        0より小さい値は0、180より大きい値は180へ修正
        """
        d = degree
        if degree < 0:
            d = 0
        elif 180 < degree:
            d = 180
        value = int(26 + (48 * d) / 90)
        wiringpi.pwmWrite(self.pin, value)
