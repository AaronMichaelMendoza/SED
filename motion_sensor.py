# File:          motion_sensor.py
# Description:   This script holds the functions used to interface with the motion sensor.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/15/2023

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

motion_pin = pyb.Pin("P0", pyb.Pin.IN, pyb.Pin.PULL_DOWN)

clock = time.clock()

def detect_motion():
    if (motion_pin == 1):
        print('MOTION DETECTED')

while(True):
    detect_motion()
