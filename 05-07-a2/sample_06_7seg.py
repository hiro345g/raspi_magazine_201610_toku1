#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from package_parts import ht16k33_7seg

# -- 変数 -- #
address = ht16k33_7seg.HT16K33_DEFAULT_ADDRESS


def main():
    """HT16K33　7seg動作確認用メイン処理"""
    fd = ht16k33_7seg.init(address)

    # 全桁を 0 から 9 へカウントアップ
    for i in range(10):
        c = str(i)  # write_digit()関数には数字を渡す
        for pos in range(4):  # 桁はposで指定
            ht16k33_7seg.write_digit(fd, pos, c)  # 各桁の値を更新
        time.sleep(1)

    # 10からカウントダウン
    data = [0x00, 0x00, 0x00, 0x00]  # 4桁分のデータを用意して更新もできる
    start_num = 10
    for i in list(reversed(range(start_num))):  # カウントダウン用数字の生成
        n = '{0:04d}'.format(i)  # 0も表示する4桁の数字を作成
        for index, c in enumerate(list(n)):
            data[index] = ht16k33_7seg.get_font(c)  # 数字を7セグメントLED用の数値へ変換
        ht16k33_7seg.update(fd, data)  # 4桁を同時に更新
        time.sleep(1)

    # ドット表示の確認
    for pos in range(4):  # 桁はposで指定
        ht16k33_7seg.turn_on_dot_at_pos(fd, pos)  # ドットはturn_on_dot_at_pos()関数を使う
        time.sleep(1)

    # ドットつき文字
    data[0] = ht16k33_7seg.get_font('1')
    data[1] = ht16k33_7seg.get_font('2')
    data[2] = ht16k33_7seg.get_font('3') | ht16k33_7seg.SEVEN_SEG_PERIOD  # ここだけドットがつく
    data[3] = ht16k33_7seg.get_font('4')
    ht16k33_7seg.update(fd, data)  # 4桁を同時に更新
    time.sleep(2)

    # クリア
    data = ht16k33_7seg.clear(fd)
    ht16k33_7seg.update(fd, data)


if __name__ == '__main__':
    main()
