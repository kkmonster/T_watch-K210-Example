from fpioa_manager import *
from Maix import I2S, GPIO
from board import board_info
import audio
import sensor
import image
import time
import lcd
import os


# register i2s (i2s0) pin
fm.register(board_info.I2S_DA, fm.fpioa.I2S0_OUT_D1)
fm.register(board_info.I2S_BCK, fm.fpioa.I2S0_SCLK)
fm.register(board_info.I2S_WS, fm.fpioa.I2S0_WS)


print(os.listdir())

# init i2s (i2s0)
wav_dev = I2S(I2S.DEVICE_0)

# init audio
player = audio.Audio(path="/sd/6.wav")
player.volume(80)

# read audio info
wav_info = player.play_process(wav_dev)
print("wav file head information:", wav_info)

# config i2s according to audio info
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
wav_dev.set_sample_rate(wav_info[1])

#loop to play audio
while True:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret == 0:
        print("end")
        break
player.finish()
