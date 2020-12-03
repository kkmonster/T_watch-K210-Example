
import lcd
import time
from fpioa_manager import *
from Maix import GPIO
from board import board_info

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
but_a = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)


fm.register(13, fm.fpioa.GPIOHS1, force=True)
led_b = GPIO(GPIO.GPIOHS1, GPIO.OUT)
led_b.value(1)  # LED is Active Low

fm.register(12, fm.fpioa.GPIOHS2, force=True)
led_r = GPIO(GPIO.GPIOHS2, GPIO.OUT)
led_r.value(1)  # LED is Active Low

fm.register(15, fm.fpioa.GPIOHS3, force=True)
led_g = GPIO(GPIO.GPIOHS3, GPIO.OUT)
led_g.value(1)  # LED is Active Low


lcd.init()

while(True):

    while but_a.value() == 1:

        led_r.value(1)
        led_g.value(1)
        led_b.value(1)
    while but_a.value() == 0:
        time.sleep(0.1)

    while but_a.value() == 1:
        led_r.value(0)
        led_g.value(1)
        led_b.value(1)

    while but_a.value() == 0:
        time.sleep(0.1)

    while but_a.value() == 1:
        led_r.value(1)
        led_g.value(1)
        led_b.value(1)
    while but_a.value() == 0:
        time.sleep(0.1)
