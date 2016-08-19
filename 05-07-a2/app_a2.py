#!/usr/bin/env python
# -*- coding: utf-8 -*-
from package_parts import ht16k33_7seg
from package_parts.parts import Speaker
import sys, time

# -- 定数宣言 -- #
HT16K33_ADDRESS = ht16k33_7seg.HT16K33_DEFAULT_ADDRESS  # LEDマトリクスドライバー I2Cアドレス
SPK_PIN = 5  # 圧電スピーカーのGPIO番号
INTERVAL = 1
MELODY_LIST = [
    ((262, 0.5), (0, 0.5), (262, 0.5), (0, 0.5), (262, 0.5), (0, 0.5), (787, 0.5)),
    ((440, 5),),
]


# -- 関数 -- #
def init():
    """ 7セグメントLED、ソフトウェアトーン初期化 """
    address = HT16K33_ADDRESS
    fd = ht16k33_7seg.init(address)
    # ソフトウェアトーン初期化
    speaker = Speaker(SPK_PIN)
    return fd, speaker


def count_down(fd_7seg, count):
    """カウントダウン"""
    data = [0x00, 0x00, 0x00, 0x00]  # 4桁分のデータを用意して更新もできる
    start_num = count
    for i in list(reversed(range(start_num))):  # カウントダウン用数字の生成
        n = i + 1  # 指定された数字から開始するには +1 が必要
        display_num = '{0:04d}'.format(n)  # 0も表示する4桁の数字を作成
        for index, c in enumerate(list(display_num)):
            data[index] = ht16k33_7seg.get_font(c)  # 数字を7セグメントLED用の数値へ変換
        ht16k33_7seg.update(fd_7seg, data)  # 4桁を同時に更新
        time.sleep(INTERVAL)
    # クリア
    data = ht16k33_7seg.clear(fd_7seg)
    ht16k33_7seg.update(fd_7seg, data)


def main(count):
    """メイン処理
    """
    fd_7seg, speaker = init()
    print('app_a1 start')
    speaker.play(MELODY_LIST[0])
    count_down(fd_7seg, count)
    speaker.play(MELODY_LIST[1])
    print('app_a1 stop')


if __name__ == '__main__':  # このファイルがスクリプトとして実行される時だけ処理を実行
    argv_count = 180
    if len(sys.argv) > 1:
        argv_count = int(sys.argv[1])
    main(argv_count)
