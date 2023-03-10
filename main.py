# File:          main.py
# Description:   This script is the main loop that the OpenMV camera runs when powered.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/2/2023
# Last Modified: 3/3/2023

# Data Abstraction:
#   - Import libraries, most notably the TensorFlowLite library
#   - Upload trained neural network from SD card
#   - Initialize variables and sensors as necessary
# Input:
#   - No user input
# Output:
#   - Voltages to pins 7, 8, and 9 to power a multi-colored LED based on the state of the
#     device
#   - Voltage to pin 0 to fire a relay if the object is classified as a human or vehicle.
# Assumptions:
#   - It is assumed that the user has a trained neural network, preferably a convolutional
#     neural network (CNN).
#   - It is assumed that the OpenMV has a motion and distance sensor connected to it for
#     interface.
#   - It is assumed that the OpenMV is connected to other necessary components for the
#     Smart Exit Device.


################# INITIALIZATION #################
# Import libraries
import sensor, image, time, pyb

# Initialize OpenMV
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# Initialize pins
relay = pyb.Pin("P0", pyb.Pin.OUT_PP)
green = pyb.Pin("P7", pyb.Pin.OUT_PP)
blue = pyb.Pin("P8", pyb.Pin.OUT_PP)
red = pyb.Pin("P9", pyb.Pin.OUT_PP)

# Initialize distance sensor

# Initialize motion sensor

# Initialize clock
clock = time.clock()


################# FUNCTION DEFINITIONS #################
# updateLED()
# description: updates the color of the LED based on the
#              current state of the device
# input: current color of LED
# output: new color of LED
def updateLED(curState):
    if (curState == IDLE)
        green.low()
        blue.low()
        red.low()
    elif (curState == CENTER)
        green.low()
        blue.toggle()
        red.low()
    elif (curState == CLASSIFY)
        green.low()
        blue.high()
        red.low()
    elif (curState == FAIL)
        green.low()
        blue.low()
        red.high()
    elif (curState == OPEN)
        green.high()
        blue.low()
        red.low()


################# MAIN #################
while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())

    # Initialize device
    curState = IDLE
    updateLED(curState)

    # State machine
    if (curState == IDLE and #motion detected):
        curState = CENTER
        updateLED(curState)
    elif (curState == CENTER):
        if (#object in DS line):
            if (#object in range):
                curState = CLASSIFY
                updateLED(curState)
        else:
            if (#no motion detected):
                curState = IDLE
                updateLED(curState)
    elif (curState == CLASSIFY):
        # classify()
        if (#person or vehicle):
            curState == OPEN
        else
            curState == FAIL
        updateLED(curState)
    elif (curState == OPEN):
        #wait
    elif (curState == FAIL):
        if (#no object in DS line):
            curState = IDLE
        else
            curState = CENTER
        updateLED(curState)

