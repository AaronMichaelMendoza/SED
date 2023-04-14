# File:          main.py
# Description:   This script is the main loop that the OpenMV camera runs when powered.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/2/2023
# Last Modified: 4/14/2023

# Data Abstraction:
#   - Import libraries
#   - Upload trained neural network from SD card
#   - Initialize variables and sensors as necessary
# Input:
#   - No user input
#   - Input in Pin 3 is from the motion sensor
#   - Pins 4 and 5 are TX and RX from distance sensor respectively
# Output:
#   - Pins 7, 8, and 9 to power three LEDs based on the state of the
#     device
#   - Pin 0 fires a relay if the object is classified as a human or vehicle.
# Assumptions:
#   - It is assumed that the user has the team's custom trained neural network on the SD card.
#   - It is assumed that the OpenMV has a motion and distance sensor connected to it for
#     interface.
#   - It is assumed that the OpenMV is connected to other necessary components for the
#     Smart Exit Device.


################# INITIALIZATION #################
# Import libraries
import sensor, image, time, pyb, os, tf, uos, gc
from pyb import Pin
from machine import UART

# Initialize OpenMV
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time = 2000)

# Initialize pins
relay = Pin('P0', Pin.OUT_PP)
green = Pin('P7', Pin.OUT_PP)
yellow = Pin('P8', Pin.OUT_PP)
red = Pin('P9', Pin.OUT_PP)

# Initialize ADC
adc = pyb.ADC(pyb.Pin("P6"))        # create an ADC on pin P6
buf = bytearray(1)                 # create a buffer to store the samples

# Initialize distance sensor
CM_TO_FT = 0.0328084

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

packet = bytearray(1)
packet[0] = 0x42
uart.write(packet)
packet[0] = 0x57
uart.write(packet)
packet[0] = 0x02
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x01
uart.write(packet)
packet[0] = 0x06
uart.write(packet)

# Initialize motion sensor
motion_pin = Pin("P3", Pin.IN, Pin.PULL_DOWN)

# Initialize clock
clock = time.clock()

################# FUNCTION DEFINITIONS #################
# updateLED()
# description: updates the color of the LED based on the
#              current state of the device
# input: current color of LED
# output: new color of LED
def updateLED(curState):
    if (curState == IDLE):
        green.high()
        yellow.low()
        red.low()
    elif (curState == CENTER):
        green.low()
        yellow.toggle()
        red.low()
    elif (curState == CLASSIFY):
        green.low()
        yellow.high()
        red.low()
    elif (curState == FAIL):
        green.low()
        yellow.low()
        red.high()
    elif (curState == OPEN):
        green.high()
        yellow.low()
        red.low()

# LED_test()
# description: tests all three LEDs
# input: void
# output: void
def LED_test():
    print("turning green on")
    green.high()
    yellow.low()
    red.low()
    pyb.delay(1000)
    print("turning yellow on")
    green.low()
    yellow.high()
    red.low()
    pyb.delay(1000)
    print("turning red on")
    green.low()
    yellow.low()
    red.high()
    pyb.delay(1000)
    print("turning all on")
    green.high()
    yellow.high()
    red.high()
    pyb.delay(1000)

# POT_test()
# description: tests potentiometer
# input: void
# output: void
def POT_test():
    adc.read_timed(buf, 1)
    pyb.delay(100)

    for val in buf:
        voltage_val = (val / 255.0) * 3.3
        print(voltage_val)
        if (voltage_val < 1.1):
            red.high()
            yellow.low()
            green.low()
        elif (voltage_val < 2.2):
            red.low()
            yellow.high()
            green.low()
        elif (voltage_val <= 3.3):
           red.low()
           yellow.low()
           green.high()
        else:
            red.high()
            yellow.high()
            green.high()
            print("ERROR")

# basic_motion_test()
# description: tests motion sensor
# input: void
# output: void
def basic_motion_test():
    if (motion_pin.value()== 1):
        print('MOTION DETECTED')

# read_distance()
# description: reads distance
# input: void
# output: -2 if data is invalid, distance in feet if data is valid
def read_distance():
    global distance = -2
    if(uart.any()):
        bytes = uart.read()
        if(len(bytes) == 9):
            #print('Distance (ft):', ((bytes[3]*256) + (bytes[2])) * CM_TO_FT)
            #print('Signal Strength:', (bytes[5]*256) + (bytes[4]))
            distance = ((bytes[3]*256) + (bytes[2])) * CM_TO_FT
    pyb.delay(10)
    return distance

################# MAIN #################
def main():
    # Initialize device
    global curState = IDLE
    ## PUT ALL DISTANCE CONFIG STUFF HERE
    while(True):
        # Set LED color
        updateLED(curState)

        # State machine
        print('Current State:', current_state)
        if (curState == IDLE):
            if (motion_pin.value() == 1):
                curState = CENTER
                motion_detected = false
        elif (curState == CENTER):
            distance = read_distance()
            if (distance != -2):
                if (#object in range):
                    curState = CLASSIFY
            else:
                if (motion_pin.value() != 1):
                    curState = IDLE
        elif (curState == CLASSIFY):
            # classify()
            if (#person or vehicle):
                curState == OPEN
            else
                curState == FAIL
        elif (curState == OPEN):
            #wait
        elif (curState == FAIL):
            if (#no object in DS line):
                curState = IDLE
            else
                curState = CENTER

