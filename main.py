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
#   - Voltages to pins _, _, and _ to power a multi-colored LED based on the state of the
#     device
#   - Voltage to pin _ to fire a relay if the object is classified as a human or vehicle.
# Assumptions:
#   - It is assumed that the user has a trained neural network, preferably a convolutional
#     neural network (CNN).
#   - It is assumed that the OpenMV has a motion and distance sensor connected to it for
#     interface.
#   - It is assumed that the OpenMv is connected to other necessary components for the
#     Smart Exit Device.


################# INITIALIZATION #################
# Import libraries
import sensor, image, time

# Initialize OpenMV
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# Initialize pins

# Initialize distance sensor

# Initialize motion sensor

# Initialize clock
clock = time.clock()


################# FUNCTION DEFINITIONS #################
# states()
# description: states of the device
# input: current state of device
# output: new state of device
def states(x):
    state = ' '
    if(x == IDLE):
        state =
    elif(x == CENTER):
        state =
    elif(x == CLASSIFY):
        state =
    elif(x == OPEN):
        state =
    elif(x == OFF):
        usys.exit('Turning System Off...')
    else:
        x = 'ERROR'
    return game_state

################# MAIN #################
def main():
    while(True):
        clock.tick()
        img = sensor.snapshot()
        print(clock.fps())
main()
