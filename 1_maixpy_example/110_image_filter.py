# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


import sensor
import image
import lcd
import gc
import time
import uos

from fpioa_manager import fm
from Maix import I2S, GPIO
from board import board_info

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1)
BOOT_KEY = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_vflip(1)

sensor.set_windowing((240, 240))
sensor.run(1)

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
        img.negate()
        img.draw_string(10, 60, "negate", color=(255, 0, 0))
    elif cnt == 2:
        img.cartoon(seed_threshold=0.05, floating_thresholds=0.05)
        img.draw_string(10, 60, "cartoon", color=(255, 0, 0))
    elif cnt == 3:
        img.histeq(adaptive=True, clip_limit=3)
        img.draw_string(10, 60, "histeq", color=(255, 0, 0))
    elif cnt == 4:
        img.mode(1)
        img.draw_string(10, 60, "mode", color=(255, 0, 0))
    elif cnt == 5:
        thresholds = (90, 100, -128, 127, -128, 127)
        img.binary([thresholds], invert=False, zero=True)
        img.draw_string(10, 60, "binary", color=(255, 0, 0))
    elif cnt == 6:
        img.laplacian(1)
        img.draw_string(10, 60, "laplacian", color=(255, 0, 0))
    elif cnt == 7:
        img.gamma_corr(gamma=0.5, contrast=1.0, brightness=0.0)
        img.draw_string(10, 60, "gamma_corr", color=(255, 0, 0))
    elif cnt == 8:
        img.gaussian(1)
        img.draw_string(10, 60, "gaussian", color=(255, 0, 0))
    elif cnt == 9:
        img.histeq()
        img.draw_string(10, 60, "histeq", color=(255, 0, 0))
    elif cnt == 10:
        img.lens_corr(strength=1.8, zoom=1.0)
        img.draw_string(10, 60, "lens_corr", color=(255, 0, 0))
    elif cnt == 11:
        img.linpolar(reverse=False)
        img.draw_string(10, 60, "linpolar", color=(255, 0, 0))
    elif cnt == 12:
        img.logpolar(reverse=False)
        img.draw_string(10, 60, "logpolar", color=(255, 0, 0))
    elif cnt == 13:
        img.mean(1)
        img.draw_string(10, 60, "mean", color=(255, 0, 0))
    elif cnt == 14:
        img.median(1, percentile=0.5)
        img.draw_string(10, 60, "median", color=(255, 0, 0))
    elif cnt == 15:
        img.midpoint(1, bias=0.5)
        img.draw_string(10, 60, "midpoint", color=(255, 0, 0))
    elif cnt == 16:
        img.bilateral(3, color_sigma=0.1, space_sigma=1)
        img.draw_string(10, 60, "bilateral", color=(255, 0, 0))
    else:
        cnt = 0

    lcd.display(img)
