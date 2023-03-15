# File:          motion_sensor.py
# Description:   This script holds the functions used to interface with the motion sensor.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/15/2023

import sensor, image, time, pyb
from pyb import Pin

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

motion_pin = Pin("P3", Pin.IN, Pin.PULL_DOWN)

clock = time.clock()

def basic_motion_test():
    if (motion_pin.value()) == 1):
        print('MOTION DETECTED')

def motion_interrupt_callback():
    print('MOTION DETECTED ON RISING EDGE')
    return true

def detect_motion():
    ExtInt(motion_pin, ExtInt.IRQ_RISING, Pin.PULL_DOWN, motion_interrupt_callback)
