# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor
import image
import lcd
import time
from fpioa_manager import fm
from Maix import I2S, GPIO
from board import board_info

lcd.init()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_vflip(1)

sensor.run(1)
origin = (0, 0, 0, 0, 1, 0, 0, 0, 0)
edge = (-1, -1, -1, -1, 8, -1, -1, -1, -1)
sharp = (-1, -1, -1, -1, 9, -1, -1, -1, -1)
relievo = (2, 0, 0, 0, -1, 0, 0, 0, -1)

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1)
BOOT_KEY = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
cnt = 0
BOOT_KEY_pressed = 0
while True:
    if BOOT_KEY.value() == 0 and BOOT_KEY_pressed == 0:
        cnt = cnt+1
        BOOT_KEY_pressed = 1

    if BOOT_KEY.value() == 1 and BOOT_KEY_pressed == 1:
        BOOT_KEY_pressed = 0

    img = sensor.snapshot()
    if cnt == 1:
        img.conv3(edge)
        img.draw_string(10, 60, "edge", color=(255, 0, 0))
    elif cnt == 2:
        img.conv3(sharp)
        img.draw_string(10, 60, "sharp", color=(255, 0, 0))
    elif cnt == 3:
        img.conv3(relievo)
        img.draw_string(10, 60, "relievo", color=(255, 0, 0))
    else:
        cnt = 0
    lcd.display(img)
