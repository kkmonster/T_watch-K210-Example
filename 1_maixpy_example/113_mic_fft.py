import lcd
import image
from Maix import FFT
from Maix import I2S
from Maix import GPIO
from fpioa_manager import fm, board_info
import sensor
import image
import time

sensor.reset()


lcd.init()

fm.register(8,  fm.fpioa.GPIO0)
fm.register(20, fm.fpioa.I2S0_IN_D0)
fm.register(19, fm.fpioa.I2S0_WS)
fm.register(18, fm.fpioa.I2S0_SCLK)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
sample_rate = int(4000)
rx.set_sample_rate(sample_rate)
img = image.Image()
sample_points = 1024
FFT_points = 512
lcd_width = 240
lcd_height = 240
hist_num = FFT_points  # changeable
if hist_num > 240:
    hist_num = 240
hist_width = int(512 / hist_num)  # changeable
x_shift = 0
while True:
    audio = rx.record(sample_points)
    FFT_res = FFT.run(audio.to_bytes(), FFT_points)
    FFT_amp = FFT.amplitude(FFT_res)

    img = img.clear()
    x_shift = 0

    for i in range(240):
        if FFT_amp[i] > 240:
            hist_height = 240
        else:
            hist_height = FFT_amp[i]*5

        img = img.draw_rectangle(
            (x_shift, 240-hist_height, hist_width, hist_height), [255, 255, 255], 2, True)
        #img = img.draw_rectangle((x_shift,240-5,1,5),[255,255,255],1,True)
        x_shift = x_shift + hist_width
    lcd.display(img)
    time.sleep_ms(10)
