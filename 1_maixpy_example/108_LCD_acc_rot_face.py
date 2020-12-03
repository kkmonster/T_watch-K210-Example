# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


from machine import I2C
import lcd
import math
import image
import time

####################
# 019_LCD_draw_face.py

x_zero = 240//2
y_zero = 135//2
x_zero_rot = x_zero
y_zero_rot = y_zero+0


def rot(x_in, y_in, theta):
    x_rot = (x_in - x_zero) * math.cos(theta) - \
        (y_in - y_zero) * math.sin(theta) + x_zero_rot
    y_rot = (x_in - x_zero) * math.sin(theta) + \
        (y_in - y_zero) * math.cos(theta) + y_zero_rot
    return int(x_rot), int(y_rot)


def rot2(x_in1, y_in1, x_in2, y_in2, theta):
    x_rot1 = (x_in1 - x_zero) * math.cos(theta) - \
        (y_in1 - y_zero) * math.sin(theta) + x_zero_rot
    y_rot1 = (x_in1 - x_zero) * math.sin(theta) + \
        (y_in1 - y_zero) * math.cos(theta) + y_zero_rot
    x_rot2 = (x_in2 - x_zero) * math.cos(theta) - \
        (y_in2 - y_zero) * math.sin(theta) + x_zero_rot
    y_rot2 = (x_in2 - x_zero) * math.sin(theta) + \
        (y_in2 - y_zero) * math.cos(theta) + y_zero_rot
    return int(x_rot1), int(y_rot1), int(x_rot2), int(y_rot2)


def draw_face(img, theta, cnt):
    img.draw_rectangle(0, 0, 240, 135, color=(255, 255, 0), fill=True)
    if cnt < 100:
        res = rot(40, 70, theta)  # left_eye
        img.draw_circle(res[0], res[1], 42, color=(
            0, 0, 0),            thickness=2, fill=True)
        img.draw_circle(res[0], res[1], 40, color=(
            255, 255, 255),            thickness=2, fill=True)
        img.draw_circle(res[0], res[1], 30, color=(
            0, 0, 0),            thickness=2, fill=True)
        res = rot(200, 70, theta)  # right_eye
        img.draw_circle(res[0], res[1], 42, color=(
            0, 0, 0),            thickness=2, fill=True)
        img.draw_circle(res[0], res[1], 40, color=(
            255, 255, 255),            thickness=2, fill=True)
        img.draw_circle(res[0], res[1], 30, color=(
            0, 0, 0),            thickness=2, fill=True)
    else:
        res = rot2(10, 70, 80, 70, theta)
        img.draw_line(res[0], res[1], res[2], res[3],
                      color=(0, 0, 0),            thickness=10)
        res = rot2(170, 70, 250, 70, theta)
        img.draw_line(res[0], res[1], res[2], res[3],
                      color=(0, 0, 0),            thickness=10)

    res = rot2(170, 10, 240, -20, theta)
    img.draw_line(res[0], res[1], res[2], res[3],
                  color=(0, 0, 0),            thickness=15)
    res = rot2(70, 10, 0, -20, theta)
    img.draw_line(res[0], res[1], res[2], res[3],
                  color=(0, 0, 0),            thickness=15)


MPU6050_ADDRESS = 0x68  # 104
MPU6050_WHOAMI = 0x75
MPU6050_SMPLRT_DIV = 0x19
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_TEMP_OUT_H = 0x41
MPU6050_GYRO_XOUT_H = 0x43
MPU6050_USER_CTRL = 0x6A
MPU6050_PWR_MGMT_1 = 0x6B
MPU6050_PWR_MGMT_2 = 0x6C
MPU6050_CONFIG = 0x1A
MPU6050_GYRO_CONFIG = 0x1B
MPU6050_ACCEL_CONFIG = 0x1C
MPU6050_FIFO_EN = 0x23

i2c = I2C(I2C.I2C0, freq=100000, scl=30, sda=31)
devices = i2c.scan()
time.sleep_ms(10)

print("i2c found:", devices)


def write_i2c(address, value):
    i2c.writeto_mem(MPU6050_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)


def MPU6050_init():
    # write_i2c(MPU6050_PWR_MGMT_1, 0x00)
    write_i2c(MPU6050_PWR_MGMT_1, 0x01 << 7)
    time.sleep_ms(200)  # wait from restart
    write_i2c(MPU6050_PWR_MGMT_1, 0x01 << 0)
    write_i2c(MPU6050_ACCEL_CONFIG, 0x10)       # range 8g
    write_i2c(MPU6050_GYRO_CONFIG, 0x10)        # range 1000 degree/s

    write_i2c(MPU6050_CONFIG, 0x03)             # DLPF_CFG Acc44hz Gyro42Hz
    write_i2c(MPU6050_SMPLRT_DIV, 0x05)         # samppling 200 hz


def MPU6050_read():
    accel = i2c.readfrom_mem(MPU6050_ADDRESS, MPU6050_ACCEL_XOUT_H, 6)
    accel_x = (accel[0] << 8 | accel[1])
    accel_y = (accel[2] << 8 | accel[3])
    accel_z = (accel[4] << 8 | accel[5])
    if accel_x > 32768:
        accel_x = accel_x-65536
    if accel_y > 32768:
        accel_y = accel_y-65536
    if accel_z > 32768:
        accel_z = accel_z-65536
    return accel_x, accel_y, accel_z


def MPU6050_read_gyro():
    Gyro = i2c.readfrom_mem(MPU6050_ADDRESS, MPU6050_GYRO_XOUT_H, 6)
    Gyro_x = (Gyro[0] << 8 | Gyro[1])
    Gyro_y = (Gyro[2] << 8 | Gyro[3])
    Gyro_z = (Gyro[4] << 8 | Gyro[5])
    if Gyro_x > 32768:
        Gyro_x = Gyro_x-65536
    if Gyro_y > 32768:
        Gyro_y = Gyro_y-65536
    if Gyro_z > 32768:
        Gyro_z = Gyro_z-65536
    return Gyro_x, Gyro_y, Gyro_z


#####################

lcd.init()
lcd.rotation(2)
lcd.clear()

i2c = I2C(I2C.I2C0, freq=100000, scl=30, sda=31)
devices = i2c.scan()

MPU6050_init()

cnt = 0
rot_theta = 0
x = 0
y = 0
z = 0
while True:

    x, y, z = MPU6050_read()
    accel_array = [x, y, z]

    rot_theta = 0.5*rot_theta-0.5*(math.atan2(y, x))
    img = image.Image()
    draw_face(img, (3.1417/2)+rot_theta, cnt)
    lcd.display(img)
    cnt += 1
    if cnt > 200:
        cnt = 0
