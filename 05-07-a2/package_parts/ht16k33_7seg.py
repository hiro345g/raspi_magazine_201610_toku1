#
# -*- coding: utf-8 -*-
import wiringpi

# -- 定数 -- #
# HT16K33コマンド用
CMD_DATA = 0x00
CMD_SYS_SET = 0x20
CMD_BLINK = 0x80
CMD_BRIGHTNESS = 0xE0
CMD_OSCILLATOR_ON = (CMD_SYS_SET | 0x01)
CMD_OSCILLATOR_OFF = (CMD_SYS_SET | 0x00)

# HT16K33アドレス
HT16K33_DEFAULT_ADDRESS = 0x70

# 点滅の指定用
HT16K33_BLINK_DISPLAY_ON = 0x01
HT16K33_BLINK_RATE_OFF = 0x00
HT16K33_BLINK_RATE_2HZ = 0x02
HT16K33_BLINK_RATE_1HZ = 0x04
HT16K33_BLINK_RATE_HALF_HZ = 0x06

# 7seg用
SEVEN_SEG_PERIOD = 0x80
DIGIT_ADDRESS = [0x00, 0x02, 0x04, 0x06]

SEVEN_SEG_FONT = {
    '0': 0x3F,  # 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, ----, ----
    '1': 0x06,  # ----, 0x02, 0x04, ----, ----, ----, ----, ----
    '2': 0x5B,  # 0x01, 0x02, ----, 0x08, 0x10, ----, 0x40, ----
    '3': 0x4F,  # 0x01, 0x02, 0x04, 0x08, ----, ----, 0x40, ----
    '4': 0x66,  # ----, 0x02, 0x04, ----, ----, 0x20, 0x40, ----
    '5': 0x6d,  # 0x01, ----, 0x04, 0x08, ----, 0x20, 0x40, ----
    '6': 0x7d,  # 0x01, ----, 0x04, 0x08, 0x10, 0x20, 0x40, ----
    '7': 0x07,  # 0x01, 0x02, 0x04, ----, ----, ----, ----, ----
    '8': 0x7F,  # 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, ----
    '9': 0x6F,  # 0x01, 0x02, 0x04, 0x08, ----, 0x20, 0x40, ----
}

# -- 変数 -- #
address = HT16K33_DEFAULT_ADDRESS
app_display_on = HT16K33_BLINK_DISPLAY_ON  # 1:on, 0: off
app_blink_rate = HT16K33_BLINK_RATE_OFF  # 0:Blink off, 2:2Hz, 4:1Hz, 6:0.5Hz
app_brightness = 0x0F  # brightness (0x00 - 0x0F)


def ht_cmd(fd, cmd, argv):
    """HT16K33へのコマンド実行"""
    ret = wiringpi.wiringPiI2CWrite(fd, cmd | argv)


def init(address):
    """HT16K33初期化処理"""
    # wiringpi.wiringPiSetup() は __init__.pyで実行済み
    fd = wiringpi.wiringPiI2CSetup(address)
    if fd == -1:
        print('wiringPiI2CSetup error')
        return -1
    set_ocillator(fd, True)
    set_display(fd, app_display_on, app_blink_rate)
    set_brightness(fd, app_brightness)
    clear(fd)
    return fd


def set_brightness(fd, brightness=0x0F):
    """HT16K33　明るさ設定"""
    brightness = int(brightness) % 0x10
    ht_cmd(fd, CMD_BRIGHTNESS | brightness, 0)


def set_display(fd, display_on=1, blink_rate=0x00):
    """HT16K33　表宇設定"""
    argv = blink_rate | display_on
    ht_cmd(fd, CMD_BLINK, argv)


def set_ocillator(fd, on=True):
    """HT16K33　オシレーター設定"""
    if on:
        ht_cmd(fd, CMD_OSCILLATOR_ON, 0)
    else:
        ht_cmd(fd, CMD_OSCILLATOR_OFF, 0)


def update(fd, data):
    """HT16K33　7seg表示更新"""
    for index, r in enumerate(DIGIT_ADDRESS):
        wiringpi.wiringPiI2CWriteReg8(fd, r, data[index])


def clear(fd):
    """HT16K33　LEDマトリクス表示用データクリア"""
    print('clear----')
    return [0x00, 0x00, 0x00, 0x00]


def get_font(c):
    """数字表示に対応する数値の取得"""
    return SEVEN_SEG_FONT.get(c)


def write_digit(fd, pos, c=None):
    """数字の表示"""
    value = get_font(c)
    pos = DIGIT_ADDRESS[pos]
    wiringpi.wiringPiI2CWriteReg8(fd, pos, value)


def turn_on_dot_at_pos(fd, pos=0):
    """posで指定された桁のドット表示"""
    pos = DIGIT_ADDRESS[pos]
    wiringpi.wiringPiI2CWriteReg8(fd, pos, SEVEN_SEG_PERIOD)

