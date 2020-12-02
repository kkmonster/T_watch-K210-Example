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

fm.fpioa.set_function(board_info.BOOT_KEY, FPIOA.GPIO7)
test_gpio = GPIO(GPIO.GPIO7, GPIO.PULL_UP)

sensor.reset()

lcd.init(color=(255, 255, 255))
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
ts.init(i2c, 1)
ts.calibrate()
lcd.clear()
img = image.Image()
img = img.invert()
status_last = ts.STATUS_IDLE
x = 0
y = 0
x_last = 0
y_last = 0
draw = False
while True:

    (status, x, y) = ts.read()
    print(status, x, y)

    if test_gpio.value() == 0:
        img = img.clear()
        img = img.invert()

    if status_last != status:
        if (status == ts.STATUS_PRESS or status == ts.STATUS_MOVE):
            draw = True
        else:
            draw = False

        status_last = status

    if draw and x_last > 0 and y_last > 0:
        img.draw_line(x_last, y_last, x, y, (0, 0, 0), 8)

    lcd.display(img)

    x_last = x
    y_last = y

    #time.sleep_ms(5)

ts.__del__()
