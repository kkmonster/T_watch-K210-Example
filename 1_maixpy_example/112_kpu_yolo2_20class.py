import sensor
import image
import lcd
import time
import KPU as kpu

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
lcd.init(freq=20000000, color=lcd.BLACK)


clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
           'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
           'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
           
# https://github.com/AiDude-io/CorgiDude/tree/master/models/yolo2
task = kpu.load(0x500000)
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.7, 0.3, 5, anchor)
while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    print(clock.fps())
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect(), (0, 255, 0), thickness=5)
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(
                    i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                lcd.draw_string(i.x(), i.y()+12, '%.3f' %
                                i.value(), lcd.RED, lcd.WHITE)
    else:
        a = lcd.display(img)

a = kpu.deinit(task)
