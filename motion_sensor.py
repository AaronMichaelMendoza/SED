# File:          motion_sensor.py
# Description:   This script holds the functions used to interface with the motion sensor.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/15/2023

import sensor, image, time, pyb, machine
from pyb import Pin
from pyb import ExtInt

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

motion_pin = Pin("P3", Pin.IN, Pin.PULL_DOWN)
rtc = pyb.RTC()

def basic_motion_test():
    if (motion_pin.value()== 1):
        print('MOTION DETECTED')

def motion_interrupt_callback(line):
    print('In callback')
    global motion_detected
    motion_detected = True
    pass

######## Configure external wakeup pin for sleep ######
motion_interrupt = ExtInt(motion_pin, ExtInt.IRQ_RISING, Pin.PULL_DOWN, motion_interrupt_callback)
#######################################################

test = False

while(test):
    motion_detected = False
    enable_sleep = True
    if (enable_sleep):
        machine.sleep()
        time.sleep_ms(1)
        if (motion_detected):
            rtc.wakeup(None)
            print("Motion detected. Waking up!!!!")
            motion_detected = False
            test = False
    else:
        img = sensor.snapshot()
        if (motion_detected):
            print("Motion detected!!!!")
            motion_detected = False
