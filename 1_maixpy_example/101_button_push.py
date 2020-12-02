# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


import lcd
from Maix import I2S, GPIO
from fpioa_manager import fm
from board import board_info

lcd.init()
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1)
BOOT_KEY = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

BOOT_KEY_pressed = 0

while(True):

    if BOOT_KEY.value() == 0 and BOOT_KEY_pressed == 0:
        print("BOOT_KEY_push")
        BOOT_KEY_pressed = 1
    if BOOT_KEY.value() == 1 and BOOT_KEY_pressed == 1:
        print("BOOT_KEY_release")
        BOOT_KEY_pressed = 0
