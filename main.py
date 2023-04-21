# File:          main.py
# Description:   This script is the main loop that the OpenMV camera runs when powered.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/2/2023
# Last Modified: 4/21/2023

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
red = Pin('P7', Pin.OUT_PP)
yellow = Pin('P8', Pin.OUT_PP)
green = Pin('P9', Pin.OUT_PP)
yellow_on = False
led_counter = 0
LED_MAX = 2

# Load CNN Model
CONFIDENCE_THRESHOLD = 0.8
net = None
labels = None
try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    #print(e)
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
    global led_counter
    global LED_MAX
    global yellow_on
    if (curState == 'IDLE'):
        green.low()
        yellow.low()
        red.low()
    elif (curState == 'CONFIG'):
        green.high()
        yellow.high()
        red.high()
    elif (curState == 'BASELINE'):
        if (yellow_on == True) and (led_counter >= LED_MAX*10):
            yellow.low()
            red.low()
            green.low()
            yellow_on = False
            led_counter = 0;
        elif (yellow_on == False) and (led_counter >= LED_MAX*10):
            yellow.high()
            green.high()
            red.high()
            yellow_on = True
            led_counter = 0;
        else:
            led_counter += 1
    elif (curState == 'CENTER'):
        green.low()
        if (yellow_on == True) and (led_counter >= LED_MAX):
            yellow.low()
            yellow_on = False
            led_counter = 0;
        elif (yellow_on == False) and (led_counter >= LED_MAX):
            yellow.high()
            yellow_on = True
            led_counter = 0;
        else:
            led_counter += 1
        red.low()
    elif (curState == 'CLASSIFY'):
        green.low()
        yellow.high()
        red.low()
    elif (curState == 'FAIL'):
        print('FAIL')
        green.low()
        yellow.low()
        red.high()
    elif (curState == 'OPEN'):
        green.high()
        yellow.low()
        red.low()

# LED_test()
# description: tests all three LEDs
# input: void
# output: void
def LED_test():
    #print("turning green on")
    green.high()
    yellow.low()
    red.low()
    pyb.delay(1000)
    #print("turning yellow on")
    green.low()
    yellow.high()
    red.low()
    pyb.delay(1000)
    #print("turning red on")
    green.low()
    yellow.low()
    red.high()
    pyb.delay(1000)
    #print("turning all on")
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
        #print(voltage_val)
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
            #print("ERROR")

# basic_motion_test()
# description: tests motion sensor
# input: void
# output: void
def basic_motion_test():
    while(True):
        if (motion_pin.value()== 0) and (motion_pin.value() == 1):
            print('MOTION DETECTED')

# read_distance()
# description: reads distance
# input: void
# output: -2 if data is invalid, distance in feet if data is valid
def read_distance():
    global distance

    MAX_UART_ATTEMPTS = 20
    num_attempts = 0

    distance = -2
    while(num_attempts < MAX_UART_ATTEMPTS):
        if(uart.any()):
            bytes = uart.read()
            for i in range(len(bytes)-3):
                if(bytes[i] == 0x59) and (bytes[i+1] == 0x59):
                    distance = ((bytes[i+3]*256) + (bytes[i+2])) * CM_TO_FT
                    break
        else:
            num_attempts += 1
            #print('UART not available')
    if(distance > 2000):
        distance = -2
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

# fire_relay_test()
# description: tests if the relay can be fired
# input: void
# output: fires relay 10 times
def fire_relay_test():
    MAX_COUNT = 10
    for i in range(MAX_COUNT):
        green.high()
        pyb.delay(1000)
        green.low()
        pyb.delay(1000)

# config_range_test()
# description: tests the configurability of the range
# input: void
# output: whether or not distance read is in range
def config_range_test():
    CONFIG_TIME = 10
    start_time = time.time()
    cur_time = time.time()
    end_time = time.time() + CONFIG_TIME
    while (cur_time < end_time):
        config_voltage = read_config_voltage()
        if (config_switch.value() == 0):
            min_distance = MIN_DIST_CONST + MAX_DIST_CONST/MAX_V_IN * config_voltage
            print('Minimum Distance:', min_distance)
        else:
            max_distance = min_distance = MIN_DIST_CONST + MAX_DIST_CONST/MAX_V_IN * config_voltage
            print('Maximum Distance:', max_distance)
        cur_time = time.time()
    print('FINAL MINIMUM DISTANCE:', min_distance)
    print('FINAL MAXIMUM DISTANCE:', max_distance)
    while(true):
        distance = read_distance()
        if distance < min_distance:
            print('Below minimum distance! Cur dist: ', distance, 'Min dist: ', min_distance)
        elif distance > max_distance:
            print('Above maximum distance! Cur dist: ', distance, 'Max dist: ', min_distance)
        else:
            print('Cur dist: ', distance)

# processsing_time_test()
# description: runs main() a certain number of times and prints out the time it takes to go from
#              IDLE to PASS/FAIL
# input: void
# output: elapsed time in ms from IDLE to PASS/FAIL
def processing_time_test():
    global curState
    global led_counter
    global CONFIDENCE_THRESHOLD
    curState = 'IDLE'
    objInRangeCount = 0
    noObjInRangeCount = 0
    noMotionCount = 0
    curTest = 0

    NUM_TESTS = 10
    REDUNDANCY_CENTER_CHECK = 50
    REDUNDANCY_MOTION_CHECK = 50
    MIN_DIST_CONST = 0.3
    MAX_DIST_CONST = 39.7
    MAX_V_IN = 3.3
    CONFIG_TIME = 10
    BASELINE_TIME = 5
    BASELINE_DISTANCE = 0
    BASELINE_THRESHOLD = 0.5

    # Configure min and max distance
    max_distance = 40;
    min_distance = 0;

    # Get baseline distance
    BASELINE_DISTANCE = 0;
    #print('Baseline Distance =', BASELINE_DISTANCE)

    while(curTest < NUM_TESTS):
        # Set LED color
        updateLED(curState)

        # State machine
        #print('Current State:', curState)
        if (curState == 'IDLE'):
            start = pyb.millis() # Get starting time
            if (motion_pin.value() == 1):
                curState = 'CENTER'
        elif (curState == 'CENTER'):
            distance = read_distance()
            #print('Center State Distance Value:', distance)
            if (distance != -2 and (distance <= BASELINE_DISTANCE - BASELINE_THRESHOLD or distance >= BASELINE_DISTANCE + BASELINE_THRESHOLD)):
                if (min_distance <= distance and distance <= max_distance):
                    objInRangeCount += 1
                if (objInRangeCount == REDUNDANCY_CENTER_CHECK):
                    curState = 'CLASSIFY'
                    objInRangeCount = 0
            else:
                if (motion_pin.value() != 1):
                    noMotionCount += 1
                    if (noMotionCount == REDUNDANCY_MOTION_CHECK):
                        curState = 'IDLE'
                        noMotionCount = 0
        elif (curState == 'CLASSIFY'):
            img = sensor.snapshot()
            for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                predictions_list = list(zip(labels, obj.output()))

                # Person detected:
                if (predictions_list[1][1] > CONFIDENCE_THRESHOLD):
                    #print('Person Detected with', predictions_list[1][1], 'confidence')
                    curState = 'OPEN'
                # Vehicle detected:
                elif (predictions_list[2][1] > CONFIDENCE_THRESHOLD):
                    #print('Vehicle Detected with', predictions_list[1][1], 'confidence')
                    curState = 'OPEN'
                else:
                    curState = 'FAIL'
        elif (curState == 'OPEN' or curState == 'FAIL'):
            curTest += 1
            print('Processing time for test ', curTest, ': ', pyb.elapsed_millis(start))
            pyb.delay(3000)
            curState = 'IDLE'
        pyb.delay(100)

# classify_test()
# description: tells whether or not a vehicle/person is identified in the image
# input: void
# output: if object is person, vehicle, or nothing with accuracy
def classify_test():
    NUM_PERSON_DETECTIONS = 3
    NUM_VEHICLE_DETECTIONS = 3
    flag = False
    while(True):
        img = sensor.snapshot()
        for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
            predictions_list = list(zip(labels, obj.output()))

            # Person detected:
            if (predictions_list[1][1] > CONFIDENCE_THRESHOLD):
                print('Person Detected with', predictions_list[1][1], 'confidence')
                person_count += 1
            # Vehicle detected:
            elif (predictions_list[2][1] > CONFIDENCE_THRESHOLD):
                print('Vehicle Detected with', predictions_list[1][1], 'confidence')
                vehicle_count += 1

        print('\nPerson count:', person_count, 'Vehicle count:', vehicle_count)
        if person_count >= NUM_PERSON_DETECTIONS:
            flag = True
            print('Person classified')
        elif vehicle_count >= NUM_VEHICLE_DETECTIONS:
            flag = True
            print('Vehicle classified')
        else:
            flag = False
        person_count = 0
        vehicle_count = 0
        if flag:
            green.high()
            pyb.delay(2000)
            green.low()
            flag = false

# optimal_classification_test()
# description: tests a certain number of times within a 5-20 ft range to see if accuracy
#              is above 70% where accuracy is defined as accurate classifications/total tests
# input: void
# output: if object is person, vehicle, or nothing with accuracy
def optimal_classification_test():
    global curState
    global led_counter
    global CONFIDENCE_THRESHOLD
    curState = 'IDLE'
    objInRangeCount = 0
    noObjInRangeCount = 0
    noMotionCount = 0
    curTest = 0
    person = False
    person_count = 0
    vehicle = False
    vehicle_count = 0
    nothing = False
    nothing_count = 0

    DESIRED_OBJECT = 'PERSON'
    NUM_TESTS = 10
    REDUNDANCY_CENTER_CHECK = 50
    REDUNDANCY_MOTION_CHECK = 50
    MIN_DIST_CONST = 0.3
    MAX_DIST_CONST = 39.7
    MAX_V_IN = 3.3
    CONFIG_TIME = 20
    BASELINE_TIME = 5
    BASELINE_DISTANCE = 0
    BASELINE_THRESHOLD = 0.5

    # Configure min and max distance.
    # "Optimal" was defined as 5-20 feet by the client
    max_distance = 20;
    min_distance = 5;

    # Get baseline distance
    BASELINE_DISTANCE = 4;
    #print('Baseline Distance =', BASELINE_DISTANCE)

    while(curTest < NUM_TESTS):
        # Set LED color
        updateLED(curState)

        # State machine
        #print('Current State:', curState)
        if (curState == 'IDLE'):
            if (motion_pin.value() == 1):
                curState = 'CENTER'
        elif (curState == 'CENTER'):
            distance = read_distance()
            #print('Center State Distance Value:', distance)
            if (distance != -2 and (distance <= BASELINE_DISTANCE - BASELINE_THRESHOLD or distance >= BASELINE_DISTANCE + BASELINE_THRESHOLD)):
                if (min_distance <= distance and distance <= max_distance):
                    objInRangeCount += 1
                if (objInRangeCount == REDUNDANCY_CENTER_CHECK):
                    curState = 'CLASSIFY'
                    objInRangeCount = 0
            else:
                if (motion_pin.value() != 1):
                    noMotionCount += 1
                    if (noMotionCount == REDUNDANCY_MOTION_CHECK):
                        curState = 'IDLE'
                        noMotionCount = 0
        elif (curState == 'CLASSIFY'):
            img = sensor.snapshot()
            for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                predictions_list = list(zip(labels, obj.output()))

                # Person detected:
                if (predictions_list[1][1] > CONFIDENCE_THRESHOLD):
                    #print('Person Detected with', predictions_list[1][1], 'confidence')
                    curState = 'OPEN'
                    person = True
                # Vehicle detected:
                elif (predictions_list[2][1] > CONFIDENCE_THRESHOLD):
                    #print('Vehicle Detected with', predictions_list[1][1], 'confidence')
                    curState = 'OPEN'
                    person = True
                else:
                    curState = 'FAIL'
                    nothing = True
        elif (curState == 'OPEN' or curState == 'FAIL'):
            curTest += 1
            if person:
                print('Person detected for test ', curTest, ': ')
                person_count += 1
            elif vehicle:
                print('Vehicle detected for test ', curTest, ': ')
                vehicle_count += 1
            else:
                print('Nothing detected for test ', curTest, ': ')
                nothing_count += 1
            pyb.delay(3000)
            curState = 'IDLE'
        pyb.delay(100)
    print('Person detections: ', person_count)
    print('Vehicle detections: ', vehicle_count)
    print('Person detections: ', nothing_count)
    if DESIRED_OBJECT == 'PERSON':
        print('Classification accuracy: ', person_count/NUM_TESTS*100, '%')
    elif DESIRED_OBJECT == 'VEHICLE':
        print('Classification accuracy: ', vehicle_count/NUM_TESTS*100, '%')
    else:
        print('Classification accuracy: ', nothing_count/NUM_TESTS*100, '%')

################# MAIN #################
def main():
    # Initialize device
    global curState
    global led_counter
    global CONFIDENCE_THRESHOLD
    curState = 'IDLE'
    person_count = 0
    vehicle_count = 0
    objInRangeCount = 0
    noObjInRangeCount = 0
    noMotionCount = 0

    REDUNDANCY_CENTER_CHECK = 10
    REDUNDANCY_MOTION_CHECK = 10
    MIN_DIST_CONST = 0.3
    MAX_DIST_CONST = 39.7
    MAX_V_IN = 3.3
    CONFIG_TIME = 20
    BASELINE_READINGS = 5
    BASELINE_DISTANCE = 0
    BASELINE_THRESHOLD = 0.5
    OPEN_TIME = 2000
    FAIL_TIME = 2000
    NUM_PERSON_DETECTIONS = 3
    NUM_VEHICLE_DETECTIONS = 3
    NUM_ATTEMPTS = 5


    # Configure min and max distance
    curState = 'CONFIG'
    start_config = False
    config_range = False
    while(True):
        updateLED(curState)
        config_voltage = read_config_voltage()
        #print(config_switch.value())
        if (config_switch.value() == 0 and config_range == False):
            min_distance = MAX_DIST_CONST - (MAX_DIST_CONST - MIN_DIST_CONST) * config_voltage/MAX_V_IN
            print('Minimum Distance:', min_distance)
            start_config = True
        elif (config_switch.value() == 1 and start_config == True):
            max_distance = MAX_DIST_CONST - (MAX_DIST_CONST - MIN_DIST_CONST) * config_voltage/MAX_V_IN
            print('Maximum Distance:', max_distance)
            config_range = True
        elif (config_switch.value() == 0 and config_range == True):
            #print('Done configuring')
            break

    print('\nMaximum Distance:', max_distance)
    print('Minimum Distance:', min_distance)
    red.low()
    green.low()
    yellow.low()

    # Get baseline distance
    count = 0
    curState = 'BASELINE'
    #print('Setting Baseline Distance')
    while (True):
        updateLED(curState)
        distance = read_distance()
        if (distance != -2):
            BASELINE_DISTANCE += distance
            count += 1
        else:
            count = 0
        if (count == BASELINE_READINGS):
            break
    BASELINE_DISTANCE = BASELINE_DISTANCE / BASELINE_READINGS
    #print('Baseline Distance =', BASELINE_DISTANCE)

    curState = 'IDLE'
    while(True):
        # Set LED color
        updateLED(curState)

        # State machine
        #print('Current State:', curState)
        if (curState == 'IDLE'):
            if (motion_pin.value() == 1):
                curState = 'CENTER'
        elif (curState == 'CENTER'):
            distance = read_distance()
            print('Center State Distance Value:', distance)
            print(curState)
            if (distance != -2 and (distance <= BASELINE_DISTANCE - BASELINE_THRESHOLD or distance >= BASELINE_DISTANCE + BASELINE_THRESHOLD)):
                if (min_distance <= distance and distance <= max_distance):
                    objInRangeCount += 1
                if (objInRangeCount == REDUNDANCY_CENTER_CHECK):
                    curState = 'CLASSIFY'
                    objInRangeCount = 0
            else:
                if (motion_pin.value() != 1):
                    noMotionCount += 1
                    if (noMotionCount == REDUNDANCY_MOTION_CHECK):
                        curState = 'IDLE'
                        noMotionCount = 0
        elif (curState == 'CLASSIFY'):
            for i in range(NUM_ATTEMPTS):
                img = sensor.snapshot()
                for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                    predictions_list = list(zip(labels, obj.output()))

                    # Person detected:
                    if (predictions_list[1][1] > CONFIDENCE_THRESHOLD):
                        print('Person Detected with', predictions_list[1][1], 'confidence')
                        person_count += 1
                    # Vehicle detected:
                    elif (predictions_list[2][1] > CONFIDENCE_THRESHOLD):
                        print('Vehicle Detected with', predictions_list[1][1], 'confidence')
                        vehicle_count += 1

            print('\nPerson count:', person_count, 'Vehicle count:', vehicle_count)
            if person_count >= NUM_PERSON_DETECTIONS:
                curState = 'OPEN'
                print('Person classified')
            elif vehicle_count >= NUM_VEHICLE_DETECTIONS:
                curState = 'OPEN'
                print('Vehicle classified')
            else:
                curState = 'FAIL'
            print(curState)
            person_count = 0
            vehicle_count = 0


        elif (curState == 'OPEN'):
            pyb.delay(OPEN_TIME)
            curState = 'IDLE'
        elif (curState == 'FAIL'):
            distance = read_distance()
            if (distance != -2) and ((distance >= BASELINE_DISTANCE - BASELINE_THRESHOLD) and (distance <= BASELINE_DISTANCE + BASELINE_THRESHOLD)):
                noObjInRangeCount += 1
                if (noObjInRangeCount == REDUNDANCY_CENTER_CHECK):
                    curState = 'IDLE'
            else:
                curState = 'CENTER'
            pyb.delay(FAIL_TIME)
        pyb.delay(100)

main()
