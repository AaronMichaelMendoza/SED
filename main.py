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
#   - Pins 7, 8, and 9 to power three LEDs based on the state of the device
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
config_switch = Pin('P1', Pin.IN, Pin.PULL_DOWN)
green = Pin('P7', Pin.OUT_PP)
yellow = Pin('P8', Pin.OUT_PP)
red = Pin('P9', Pin.OUT_PP)

# Load CNN Model
CONFIDENCE_THRESHOLD = 0.5
net = None
labels = None
try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')


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

# read_config_voltage()
# description: reads config voltage
# input: void
# output: voltage from pot
def read_config_voltage():
    global config_voltage
    adc.read_timed(buf, 1)
    pyb.delay(100)

    for val in buf:
        config_voltage = (val / 255.0) * 3.3
    return config_voltage

################# MAIN #################
def main():
    # Initialize device
    global curState = IDLE
    objInRangeCount = 0
    noObjInRangeCount = 0
    noMotionCount = 0

    REDUNDANCY_CHECK = 5
    MIN_DIST_CONST = 0.3
    MAX_DIST_CONST = 39.7
    MAX_V_IN = 3.3
    CONFIG_TIME = 20
    BASELINE_TIME = 5
    BASELINE_DISTANCE = 0

    # Configure min and max distance
    start_time = time.time()
    cur_time = time.time()
    end_time = time.time() + CONFIG_TIME
    while (cur_time < end_time):
        red.high()
        green.high()
        yellow.high()
        config_voltage = read_config_voltage()
        if (config_switch.value() == 0):
            min_distance = MIN_DIST_CONST + MAX_DIST_CONST/MAX_V_IN * config_voltage
        elif:
            max_distance = min_distance = MIN_DIST_CONST + MAX_DIST_CONST/MAX_V_IN * config_voltage
    red.low()
    green.low()
    yellow.low()

    # Get baseline distance
    start_time = time.time()
    cur_time = time.time()
    end_time = time.time() + BASELINE_TIME
    count = 0
    while (cur_time < end_time):
        # LED control
        if (cur_time < end_time - 2):
            red.high()
        elif (cur_time < end_time < 4):
            red.low()
            yellow.high()
        else:
            yellow.low()
            gree.high()
        distance = read_distance()
        BASELINE_DISTANCE += distance
        count += 1
    BASELINE_DISTANCE = BASELINE_DISTANCE / count

    while(True):
        # Set LED color
        updateLED(curState)

        # State machine
        print('Current State:', current_state)
        if (curState == IDLE):
            if (motion_pin.value() == 1):
                curState = CENTER
        elif (curState == CENTER):
            distance = read_distance()
            if (distance != -2 and distance >= BASELINE_DISTANCE - 0.5 and distance <= BASELINE_DISTANCE + 0.5):
                if (min_distance <= distance and distance <= max_distance):
                    objInRangeCount += 1
                if (objInRangeCount == REDUNDANCY_CHECK):
                    curState = CLASSIFY
                    objInRangeCount = 0
            else:
                if (motion_pin.value() != 1):
                    noMotionCount += 1
                    if (noMotionCount == REDUNDANCY_CHECK):
                        curState = IDLE
                        noMotionCount = 0
        elif (curState == CLASSIFY):
            img = sensor.snapshot()
            for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                predictions_list = list(zip(labels, obj.output()))

                # Person detected:
                if (predictions_list[1][1] > CONFIDENCE_THRESHOLD):
                    print('Person Detected with', predictions_list[1][1], 'confidence')
                    curState == OPEN
                # Vehicle detected:
                elif (predictions_list[2][1] > CONFIDENCE_THRESHOLD):
                    print('Vehicle Detected with', predictions_list[1][1], 'confidence')
                    curState == OPEN
                else
                    curState == FAIL
        elif (curState == OPEN):
            pyd.delay(5000)
            curState = IDLE
        elif (curState == FAIL):
            distance = read_distance()
            if (distance == -2):
                noObjInRangeCount += 1
                if (noObjInRangeCount == REDUNDANCY_CHECK):
                    curState = IDLE
            else
                curState = CENTER

