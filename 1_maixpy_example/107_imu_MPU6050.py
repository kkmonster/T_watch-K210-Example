# Copyright (c) 2019 aNoken
# https://anoken.jimdo.com/
# https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from machine import I2C
import lcd
import time

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


MPU6050_init()

lcd.init()
lcd.clear()

aRes = 8.0/32768.0
gyroRes = 1000/32768.0

while True:
    ax, ay, az = MPU6050_read()
    accel_array = [ax*aRes, ay*aRes, az*aRes]
    print(accel_array)
    lcd.draw_string(20, 50, "ax:"+str(accel_array[0]))
    lcd.draw_string(20, 70, "ay:"+str(accel_array[1]))
    lcd.draw_string(20, 90, "az:"+str(accel_array[2]))

    gx, gy, gz = MPU6050_read_gyro()
    gyro_array = [gx*aRes, gy*aRes, gz*aRes]
    print(gyro_array)
    lcd.draw_string(20, 120, "gx:"+str(gyro_array[0]))
    lcd.draw_string(20, 140, "gy:"+str(gyro_array[1]))
    lcd.draw_string(20, 160, "gz:"+str(gyro_array[2]))

    time.sleep_ms(100)
