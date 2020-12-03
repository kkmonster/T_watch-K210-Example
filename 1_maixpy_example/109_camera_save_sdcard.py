# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor
import image
import lcd
import os
from fpioa_manager import fm
import sensor
import image
import time
import lcd
import time
import touchscreen as ts
from machine import I2C
import lcd
import image
from board import board_info
from fpioa_manager import *
from Maix import FPIOA, GPIO


i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
ts.init(i2c, 1)


fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

is_button_b = 0

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_vflip(1)

sensor.run(1)

devices = os.listdir("/")
print(devices)

if "sd" in devices:
    os.chdir("/sd")
    if not "save" in os.listdir():
        os.mkdir("save")

else:
    lcd.draw_string(70, 100, "No uSD Card !!!", lcd.RED, lcd.BLACK)
    while 1:
        time.sleep(1)

path = "save/"
ext = ".jpg"
cnt = 0
img_read = image.Image()

status_last = ts.STATUS_IDLE

while True:

    (status, x, y) = ts.read()

    if status_last != status:
        if (status == ts.STATUS_PRESS):
            print("save image")
            cnt += 1
            fname = path+str(cnt)+ext
            print(fname)
            img.save(fname, quality=95)
            is_button_a = 1

    status_last = status

    if is_button_b == 1:
        lcd.display(img_read)

    else:
        img = sensor.snapshot()
        lcd.display(img)

    if but_b.value() == 0 and is_button_b == 0:
        fname = path+str(cnt)+ext
        print(fname)
        img_read = image.Image(fname)
        is_button_b = 1

    if but_b.value() == 1 and is_button_b == 1:
        is_button_b = 0
