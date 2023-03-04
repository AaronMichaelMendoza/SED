# File:          classify.py
# Description:   This script holds everything necessary to classify an object.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/3/2023

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
